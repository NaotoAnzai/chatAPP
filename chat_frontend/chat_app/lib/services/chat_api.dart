import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatApi {
  final String baseUrl = "http://localhost:8000"; // Dockerで動いているAPI

  Future<String> sendMessage(String message) async {
    final response = await http.post(
      Uri.parse("$baseUrl/chat"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"message": message}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data["reply"]; // APIの返り値に合わせて修正
    } else {
      throw Exception("Failed to send message: ${response.body}");
    }
  }
}
