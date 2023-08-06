def gitlab_branch(branch='default', topic=None):
    """Return the GitLab branch for a branch/topic combination."""
    if topic is None:
        return 'branch/' + branch
    return '/'.join(('topic', branch, topic))
