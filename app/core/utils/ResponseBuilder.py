from starlette.responses import JSONResponse

from app.core.models.DefaultResponseModel import DefaultResponseModel


class ResponseBuilder:

    @staticmethod
    def __get_response_schema(data: dict or None, info: str or None = "Все хорошо") -> dict:
        """
        Получение шаблона ответа сервера
        """
        return DefaultResponseModel(data=data, info=info).dict()

    @staticmethod
    def result(data: dict or None, info: str = "Все хорошо", status: int = 200) -> JSONResponse:
        """
        Билдер запроса по шаблону
        :param data: Данные запроса
        :param info: Дополнительная информация
        :param status: статус
        :return: JSONResponse
        """
        data = ResponseBuilder.__get_response_schema(data=data, info=info)
        return JSONResponse(status_code=status, content=data)

    @staticmethod
    def success(info: str = "Все хорошо") -> JSONResponse:
        """
        Готовый запрос, когда все хорошо
        :param info: Дополнительная информация
        :return: JSONResponse
        """
        status = 200
        data = ResponseBuilder.__get_response_schema(data=None, info=info)
        return JSONResponse(status_code=status, content=data)

    @staticmethod
    def server_error(info: str = "Внутрняя ошибка сервера") -> JSONResponse:
        """
        Готовый запрос, когда все плохо
        :param info: Дополнительная информация
        :return: JSONResponse
        """
        status = 500
        data = ResponseBuilder.__get_response_schema(data=None, info=info)
        return JSONResponse(status_code=status, content=data)

    @staticmethod
    def not_found(info: str = "Не нашел") -> JSONResponse:
        """

        :param info: Дополнительная информация
        :return: JSONResponse
        """
        status = 404
        data = ResponseBuilder.__get_response_schema(data=None, info=info)
        return JSONResponse(status_code=status, content=data)

    @staticmethod
    def not_impl(info: str = "Метод не готов") -> JSONResponse:
        """

        :param info: Дополнительная информация
        :return: JSONResponse
        """
        status = 501
        data = ResponseBuilder.__get_response_schema(data=None, info=info)
        return JSONResponse(status_code=status, content=data)

