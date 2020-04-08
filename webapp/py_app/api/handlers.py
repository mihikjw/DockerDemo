from redis import Redis
import logging


class HttpHandlers():
    "class containing HTTP API endpoint handler methods"

    HTTP_STATUS_OK = 200
    HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
    redis_client: Redis

    @staticmethod
    def visits():
        result_body = None
        result_code = -1

        if HttpHandlers.redis_client is not None:
            try:
                visits_temp = HttpHandlers.redis_client.get("visits")

                if visits_temp is not None:
                    visits = int(visits_temp)
                else:
                    visits = 0

                visits += 1
                result_body = {"visits": visits}
                result_code = HttpHandlers.HTTP_STATUS_OK
                HttpHandlers.redis_client.mset(result_body)
            except Exception as ex:
                result_body = {"error": f"ex processing request: {str(ex)}"}
                result_code = HttpHandlers.HTTP_STATUS_INTERNAL_SERVER_ERROR
        else:
            result_body = {"error": "redis_client Is None"}
            result_code = HttpHandlers.HTTP_STATUS_INTERNAL_SERVER_ERROR

        if "error" in result_body:
            logging.error(result_body["error"])

        return result_body, result_code
