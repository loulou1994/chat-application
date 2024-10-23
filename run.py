import sqlalchemy as sa
import sqlalchemy.orm as so
from chat_app import app, db
from chat_app.models import User, Message


if __name__ == "__main__":
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Message': Message,
    }
