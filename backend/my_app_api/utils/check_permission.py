from fastapi import HTTPException


def check_permission(auth):
    """Проверка прав доступа"""
    if 101 not in auth['indirect_groups']:
        raise HTTPException(
            status_code=403, detail='У вас нет прав!')
