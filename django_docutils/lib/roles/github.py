from .common import generic_url_role


def github_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to GitHub repos and issues.

    :gh:`vim-airline` ->
       link: https://github.com/vim-airline
       text: vim-airline


    :gh:`vim-airline's org <vim-airline>` ->
       link: https://github.com/vim-airline
       text: vim-airline's org

    :gh:`vim-airline/vim-airline` ->
       link: https://github.com/vim-airline/vim-airline
       text: vim-airline/vim-airline

    :gh:`vim-airline/vim-airline#134` ->
       link: https://github.com/vim-airline/vim-airline/issues/134
       text: vim-airline/vim-airline#134

    :gh:`this example issue <vim-airline/vim-airline#134>` ->
       link: https://github.com/vim-airline/vim-airline/issues/134
       text: this example issue
    """

    def url_handler(target):
        if '#' in target:
            user_n_repo, issue = target.split('#')
            if issue.isnumeric():
                return f'https://github.com/{user_n_repo}/issues/{issue}'

        return f'https://github.com/{target}'

    return generic_url_role(name, text, url_handler)
