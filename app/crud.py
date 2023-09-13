from sqlalchemy.orm import Session

import models


def create_video(db: Session, resource_id, title):
    video = models.Video(resource_id=resource_id, title=title)
    db.add(video)
    db.commit()
    return video


def get_all_video(db: Session):
    return db.query(models.Video).all()


def edit_video_downloaded_status(db: Session, resource_id, status: bool):
    video = db.query(models.Video).filter(models.Video.resource_id == resource_id).one()
    video.is_downloaded = status
    db.commit()
