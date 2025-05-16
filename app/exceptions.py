from fastapi import HTTPException, status


FileNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail=f"Указанный файл не найден")

WrongCurrencyException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                       detail="Оплата доступна только рублями RUB")

UserNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail=f"Пользователя с таким ID не существует")

TransactionAlreadyExistsException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                                  detail="Транзакция с таким id уже существует")

