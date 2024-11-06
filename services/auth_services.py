# import jwt 
# from decouple import config

# class Security():
#     secret = "key"

#     @classmethod
#     def verify_token(cls, headers):
#         if 'Authorization' in headers.keys():
#             authorization = headers['Authorization']
#             jwt_payload = authorization.split(" ")[1]
#             # print("JWT Payload:", jwt_payload)
            
#             try:
#                 return jwt.decode(jwt_payload, cls.secret, algorithms=["HS256"])
#             except jwt.ExpiredSignatureError:
#                 print("Error: The token has expired")
#                 return False
#             except (jwt.DecodeError, jwt.InvalidTokenError):
#                 print("Error: Invalid token")
#                 return False
#             except jwt.InvalidIssuerError:
#                 print("Error: Invalid issuer")
#                 return False
#         return False