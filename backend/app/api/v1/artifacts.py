"""
Artifacts API endpoints for fetching, exporting, and rendering.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.future import select
from sqlalchemy import desc

from app.api.deps import get_db
from app.db.models import ArtifactModel
from app.db.session import db_execute
from app.schemas.artifact import ArtifactResponse, ArtifactCreate
from app.core.security import ARTIFACT_CSP_HEADER, sanitize_html

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])


@router.get("/session/{session_id}", response_model=List[ArtifactResponse])
async def list_session_artifacts(
    session_id: str,
    db: Any = Depends(get_db)
):
    """Lists all artifacts generated in a given session."""
    stmt = (
        select(ArtifactModel)
        .where(ArtifactModel.session_id == session_id)
        .order_by(desc(ArtifactModel.created_at))
    )
    result = await db_execute(db, stmt)
    artifacts = result.scalars().all()

    return [
        ArtifactResponse(
            id=a.id,
            session_id=a.session_id,
            title=a.title,
            artifact_type=a.artifact_type,
            language=a.language,
            content=a.content,
            metadata_json=a.metadata_json,
            created_at=a.created_at
        )
        for a in artifacts
    ]


@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(
    artifact_id: str,
    db: Any = Depends(get_db)
):
    """Retrieves a single artifact by ID."""
    stmt = select(ArtifactModel).where(ArtifactModel.id == artifact_id)
    result = await db_execute(db, stmt)
    artifact = result.scalars().first()

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    return ArtifactResponse(
        id=artifact.id,
        session_id=artifact.session_id,
        title=artifact.title,
        artifact_type=artifact.artifact_type,
        language=artifact.language,
        content=artifact.content,
        metadata_json=artifact.metadata_json,
        created_at=artifact.created_at
    )


@router.get("/{artifact_id}/raw")
async def get_raw_artifact(
    artifact_id: str,
    db: Any = Depends(get_db)
):
    """Serves the raw HTML/Markdown artifact with Content-Security-Policy headers."""
    stmt = select(ArtifactModel).where(ArtifactModel.id == artifact_id)
    result = await db_execute(db, stmt)
    artifact = result.scalars().first()

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    if artifact.artifact_type == "html":
        clean_html = sanitize_html(artifact.content)
        return HTMLResponse(
            content=clean_html,
            headers={
                "Content-Security-Policy": ARTIFACT_CSP_HEADER,
                "X-Frame-Options": "SAMEORIGIN"
            }
        )
    else:
        return Response(
            content=artifact.content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{artifact.title.replace(" ", "_")}.md"'
            }
        )
