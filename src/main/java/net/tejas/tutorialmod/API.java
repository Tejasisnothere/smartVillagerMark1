package net.tejas.tutorialmod;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import java.io.StringReader;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;

public class API {

    private static final HttpClient client = HttpClient.newHttpClient();

    public static CompletableFuture<String> sendJSON(String message, String userID) {

        String json = String.format(
                "{\"userMessage\":\"%s\",\"userID\":\"%s\"}",
                escape(message),
                userID
        );

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/message"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenApply(body -> {
                    try(JsonReader reader = Json.createReader(new StringReader(body))){
                        JsonObject jw = reader.readObject();
                        return jw.getString("message",null);
                    }
                })
                .exceptionally(e -> {
                    System.out.println("API error: " + e.getMessage());
                    return null;
                });
    }

    public static CompletableFuture<String> selectVillager(String userID, String villagerID) {

        String json = String.format(
                "{\"villagerID\":\"%s\",\"userID\":\"%s\"}",
                villagerID, userID
        );

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/right_click"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenApply(body -> {
                    try(JsonReader reader = Json.createReader(new StringReader(body))){
                        JsonObject jw = reader.readObject();
                        return jw.getString("message",null);
                    }
                })
                .exceptionally(e -> {
                    System.out.println("API error: " + e.getMessage());
                    return null;
                });
    }

    private static String escape(String s) {
        return s.replace("\"", "\\\"");
    }
}