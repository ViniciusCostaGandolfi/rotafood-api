from fastapi import HTTPException
from fastapi import status


not_allowed_exception =  HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso Negado"
            )

not_found_exception =  HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Recurso não encontrado"
            )
