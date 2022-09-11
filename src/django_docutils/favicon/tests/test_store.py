import pytest

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db(transaction=True)
def test_stored_favicon(Favicon):
    favicon = Favicon()

    favicon_content = b"imgcontent"

    favicon.domain = "test.com"
    favicon.favicon = SimpleUploadedFile(
        name="test_image.jpg", content=favicon_content, content_type="image/ico"
    )

    favicon.save()

    f = Favicon.objects.first()
    assert f.favicon.read() == favicon_content
