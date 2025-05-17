from flask import jsonify

def format_response(status, code, message=None, data=None, error=None):
  response = {
    "status": status,
    "code": code,
  }

  if message is not None:
    response["message"] = message

  if data is not None:
    response["data"] = data
    
  if error is not None:
    response["error"] = error

  return jsonify(response), code