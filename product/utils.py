from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_video(video_object):
    if not video_object.path.endswith(".mp4"):
        raise ValidationError(
            _("Video format must be .mp4."),
        )
