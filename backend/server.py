from concurrent import futures
import grpc
import tempconv_pb2
import tempconv_pb2_grpc

class TempConvService(tempconv_pb2_grpc.TempConvServiceServicer):
    def CelsiusToFahrenheit(self, request, context):
        c = request.value
        f = (c * 9/5) + 32
        return tempconv_pb2.TempResponse(value=f)

    def FahrenheitToCelsius(self, request, context):
        f = request.value
        c = (f - 32) * 5/9
        return tempconv_pb2.TempResponse(value=c)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tempconv_pb2_grpc.add_TempConvServiceServicer_to_server(TempConvService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
