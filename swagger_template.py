template = {
  "swagger": "2.0",
  "info": {
    "title": "QA from DOC API",
    "description": "QA from DOC",
    "version": "0.0.1"
  },
  "tags": [
    {
      "name": "qa_from_doc",
      "description": "qa_from_doc"
    }
  ],
  "paths": {
    "/qa_from_doc": {
      "post": {
        "tags": [
          "qa_from_doc"
        ],
        "summary": "Answer the questions from doc",
        "description": "",
        "consumes": [
          "application/json"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "description": "text",
            "required": True,
            "schema": {
              "$ref": "#/definitions/question"
            }
          },
        ],
        "responses": {
          "200": {
            "description": "Input status",
            "schema": {
              "$ref": "#/definitions/answer"
            }
          }
        }
      }
    },
    "/upload_doc": {
      "post": {
        "tags": [
          "upload_doc"
        ],
        "summary": "",
        "description": "",
        "consumes": [
          "multipart/form-data"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "in": "formData",
            "name": "file",
            "type": "file",
            "description": "files",
            "required": True
          },
          {
            "in": "formData",
            "name": "filename",
            "type": "string",
            "description": "filename",
            "required": True
          },
        ],
        "responses": {
          "200": {
            "description": "Upload status",
            "schema": {
              "$ref": "#/definitions/upload_status"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "file": {
      "type": "object",
      "required": [
        "filename"
      ],
      "properties": {
        "filename": {
          "items": {
            "type": "string"
          },
          "example": "IAM"
        },
      }
    },
    "upload_status": {
      "type": "object",
      "properties": {
        "response": {
          "items": {
            "type": "string"
          },
          "example": "Upload success!"
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    },
    "question": {
      "type": "object",
      "properties": {
        "question": {
          "items": {
            "type": "string"
          },
          "example": "What is IAM?"
        },
        "filename": {
          "items": {
            "type": "string"
          },
          "example": "IAM"
        },
      }
    },
    "answer": {
      "type": "object",
      "properties": {
        "response": {
          "items": {
            "type": "string"
          },
          "example": "IAM is ......"
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    },
    "ApiResponse": {
      "type": "object",
      "properties": {
        "code": {
          "type": "integer",
          "format": "int32"
        },
        "type": {
          "type": "string"
        },
        "message": {
          "type": "string"
        }
      }
    }
  }
}