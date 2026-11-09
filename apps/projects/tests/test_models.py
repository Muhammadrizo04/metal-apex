from django.test import SimpleTestCase

from apps.projects.models import Video


class VideoIdTests(SimpleTestCase):
    def test_youtube_id_variants(self):
        cases = [
            ("https://www.youtube.com/watch?v=XuN47W_qGYk", "XuN47W_qGYk"),
            ("https://youtu.be/r1NFnKlrsvk?si=Q7pMxSBZhnZEHBcC", "r1NFnKlrsvk"),
            ("https://youtube.com/shorts/YIUAgnRsXHA?feature=share", "YIUAgnRsXHA"),
        ]
        for url, video_id in cases:
            self.assertEqual(Video(url=url).youtube_id, video_id)

    def test_unknown_url_gives_empty_id(self):
        self.assertEqual(Video(url="https://example.uz/video").youtube_id, "")
