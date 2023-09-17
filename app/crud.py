from sqlalchemy.orm import Session

import models


def create_video(db: Session, resource_id, title, file_path):
    video = models.Video(resource_id=resource_id, title=title, file_path=file_path)
    db.add(video)
    db.commit()
    return video


def get_video_by_resource_id(db: Session, resource_id):
    video = (
        db.query(models.Video).filter(models.Video.resource_id == resource_id).first()
    )
    return video


def get_all_video(db: Session):
    return db.query(models.Video).all()


def edit_video_downloaded_status(db: Session, resource_id, status: bool):
    video = (
        db.query(models.Video).filter(models.Video.resource_id == resource_id).first()
    )
    video.is_downloaded = status
    db.commit()
