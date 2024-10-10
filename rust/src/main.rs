use actix_web::{get, App, HttpResponse, HttpServer};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
struct Task {
    id: u32,
    name: String,
}

#[get("/tasks")]
async fn get_tasks() -> HttpResponse {
    let task = Task {
        id: 32,
        name: String::from("Hello"),
    };
    HttpResponse::Ok().json(task)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(get_tasks))
        .bind("127.0.0.1:8080")?
        .run()
        .await
}
