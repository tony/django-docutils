# Releasing

## Version Policy

django-docutils is pre-1.0. Minor version bumps may include breaking changes.
Users should pin to `>=0.x,<0.y`.

## Release Process

Releases are triggered by git tags and published to PyPI via trusted publishing.

1. Update `CHANGES` with the release notes

2. Bump version in `src/django_docutils/__about__.py`

3. Commit:

   ```console
   $ git commit -m "django-docutils <version>"
   ```

4. Tag:

   ```console
   $ git tag v<version>
   ```

5. Push:

   ```console
   $ git push && git push --tags
   ```
