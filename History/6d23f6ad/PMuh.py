
@router.post(
    "/{project_def_id}/workers",
    status_code=status.HTTP_200_OK,
    response_model=ProjectDefResponse,
)
async def create_project_user(
    workers: Workers,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> ProjectDef:
    if group in settings.TL_GROUP:
