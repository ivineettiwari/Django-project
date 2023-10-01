import jwt

key = "ksefwefjlemvDRC$%"

def encode(data):
    """
    encode user payload as a jwt
    :param user:
    :return:
    """
    try:
        if data['secret_key'] != key:
            raise Exception("Error while generating token")
        payload = {
            'email':data['email'],
            'secret_key':data['secret_key']
        }
        encoded_data = jwt.encode(payload=payload,
                                key='secret',
                                algorithm="HS256")

        return encoded_data
    except Exception as e:
        return e


def decode(token: str):
    """
    :param token: jwt token
    :return:
    """
    try: 
        decoded_data = jwt.decode(jwt=token,
                                key='secret',
                                algorithms=["HS256"])

        return decoded_data
    except Exception as e:
        return e