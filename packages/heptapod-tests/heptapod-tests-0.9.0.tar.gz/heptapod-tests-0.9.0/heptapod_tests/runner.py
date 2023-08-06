import attr
import requests

from .wait import (
    wait_assert,
)

ARTIFACT_FORMATS = dict(archive='zip',
                        trace='raw',
                        metadata='gzip',
                        )


@attr.s
class Runner:
    heptapod = attr.ib()
    running_for = attr.ib()  # Group, Project or Heptapod
    description = attr.ib()
    id = attr.ib()
    token = None  # not displayed in repr etc

    @classmethod
    def api_register(cls, running_for, description):
        """Register the runner for a given scope of projects

        :param running_for: currently only a :class:`Project` instance, should
             eventually encompass :class:`Group` instances and the whole
             Heptapod.
        """
        heptapod = running_for.heptapod

        registration_token = running_for.api_get_field('runners_token')
        assert registration_token is not None

        resp = requests.post(heptapod.api_url + '/runners',
                             data=dict(token=registration_token,
                                       description=description,
                                       active=True,
                                       run_untagged=True,
                                       tag_list=[],
                                       ))
        assert resp.status_code == 201
        as_json = resp.json()

        runner = cls(heptapod=heptapod,
                     id=as_json['id'],
                     running_for=running_for,
                     description=description)
        runner.token = as_json['token']
        return runner

    def request_job(self):
        resp = requests.post(
            self.heptapod.api_url + '/jobs/request',
            json=dict(token=self.token,
                      info=dict(
                          executor='docker',
                          features=dict(
                              # always true (shells/abstract.go)
                              upload_multiple_artifacts=True,
                              upload_raw_artifacts=True,
                              refspecs=True,
                              artifacts=True,
                              artifacts_exclude=True,
                              multi_build_steps=True,
                              return_exit_code=True,
                              raw_variables=True,
                              cache=True,
                              masking=True,
                              # true for Docker executor
                              variables=True,
                              image=True,
                              services=True,
                              session=True,
                              terminal=True,
                              # shared seems to be set to True
                              # for shell, ssh and custom only.
                              shared=False,
                              # proxy seems to be set to True
                              # for kubernetes only.
                              # TODO evaluate if we shouldn't set
                              # it for PAAS Runner
                              proxy=False,
                          )),
                      ))
        assert resp.status_code < 400
        if resp.status_code != 204:  # or == 200
            return resp.json()

    def wait_assert_one_job(self, timeout_factor=3, retry_wait_factor=0.2,
                            msg="job not given after {timeout} seconds"):
        return wait_assert(lambda: self.request_job(),
                           lambda job: job is not None,
                           timeout_factor=timeout_factor,
                           retry_wait_factor=retry_wait_factor,
                           msg=msg,
                           )

    def wait_assert_jobs(self, number, **kwargs):
        """Fetches the given number of jobs, asserting their presence.

        GitLab workers will produce the jobs asychronously (that's
        why we wait). Hence the ordering of the results makes no sense.

        :param kwargs: passed down to each calls to `wait_assert()`.
        """
        return [
            self.wait_assert_one_job(
                msg="Got only %d job(s) instead of the expected %d "
                "after waiting for {timeout} seconds per job" % (i, number),
                **kwargs)
            for i in range(number)]

    def api_get(self):
        return requests.get(
            self.heptapod.api_url + '/runners/' + str(self.id),
            # Runner token can't be used for this
            headers={'Private-Token': self.running_for.owner_token})

    def api_delete(self):
        resp = requests.delete(self.heptapod.api_url + '/runners',
                               data=dict(token=self.token))
        assert resp.status_code == 204

    def upload_artifact(self, job, fobj, artifact_type='archive'):
        artifact_format = ARTIFACT_FORMATS[artifact_type]
        resp = requests.post(
            '{base_url}/jobs/{id}/artifacts'.format(
                base_url=self.heptapod.api_url,
                **job),
            params=dict(artifact_format=artifact_format,
                        artifact_type=artifact_type),
            headers={'JOB-TOKEN': job['token']},
            files=dict(file=fobj))
        assert resp.status_code < 400
        return resp.json()

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        self.api_delete()
        return False


def job_variables(acquired_job):
    """Return job variables as a :class:`dict`.

    :param acquired_job: same :class:`dict` as acquired by a Runner
    """
    return {v['key']: v['value'] for v in acquired_job['variables']}
