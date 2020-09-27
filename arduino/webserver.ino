WiFiServer server(80);

const char* ssid = "Top Secret";
const char* password = "Heul-erg-geheim-wachtwoord";

void initWebserver() {
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address on serial monitor
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");    //URL IP to be typed in mobile/desktop browser
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

void checkForWebActivatie() {
  WiFiClient client = server.available();  
  if (!client) {
    return;
  }
  Serial.println("new client");
  while (!client.available()) {
    delay(1);
  }
  // Read the first line of the request
  String webRequest = client.readStringUntil('\r');
  Serial.println(webRequest);
  client.flush();
  
  responceOnWeb(webRequest);
  
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html style=\"background-color:black; color:white;\">");
  client.println("<h1 align=center>stapBaseper motor controlled</h1>");
  client.println("<h2 align=center>Pasibun</h2><br><br>");
  client.print("<span style=\"margin-left:46%;\">Base moving= ");

  if (valueForBase == HIGH) {
    client.print("Links</span>");
  } else {
    client.print("Rechts</span>");
  }
  client.println("<br><br>");
  client.println("<a style=\"margin-left:45%;\" href=\"/Command=forward-base\"\"><button>Links </button></a>");
  client.println("<a style=\"display:block;margin-left:50%;margin-top:-21px;\" href=\"/Command=backward-base\"\"><button>Rechts </button></a>");

  client.print("<span style=\"margin-left:46%;\">First axle moving= ");

  if (valueForBase == HIGH) {
    client.print("Forward</span>");
  } else {
    client.print("Backward</span>");
  }
  client.println("<br><br>");
  client.println("<a style=\"margin-left:45%;\" href=\"/Command=forward-first\"\"><button>Forward </button></a>");
  client.println("<a style=\"display:block;margin-left:50%;margin-top:-21px;\" href=\"/Command=backward-first\"\"><button>Backward </button></a>");


  client.println("</html>");
  Serial.println("Client disonnected");
  Serial.println("");
}
