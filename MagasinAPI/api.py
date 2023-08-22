from config import app
import routes

routes.init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)