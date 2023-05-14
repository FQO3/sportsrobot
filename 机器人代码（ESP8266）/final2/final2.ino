#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WebServer.h>
#include <LobotServoControllerS.h>
#include <SoftwareSerial.h>
#include <FS.h>

SoftwareSerial mySerial(D6, D7);//rx tx  D6 D7
LobotServoController myse(mySerial);
ESP8266WiFiMulti wifiMulti;
ESP8266WebServer esp8266_server(80);//80端口开服

int cnt = 0;
const char *headerKeys[] = {"Content-Length", "Content-Type", "Connection", "Date"};

IPAddress local_IP(192, 168, 4, 10);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);
void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("");

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  pinMode(D0, OUTPUT);
  digitalWrite(D0, LOW);

  //  wifiMulti.addAP("lhz", "15801601650");
  wifiMulti.addAP("esp32", "12345678");
  Serial.println(WiFi.config(local_IP, gateway, subnet));
  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // 尝试进行wifi连接。
    delay(70);
    Serial.print(i++); Serial.print(' ');
  }
  digitalWrite(D0, HIGH);
  for (int i = 1; i <= 3; i++)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
  }
  digitalWrite(LED_BUILTIN, LOW);

  // WiFi连接成功后将通过串口监视器输出连接成功信息
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());              // 通过串口监视器输出连接的WiFi名称
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // 通过串口监视器输出ESP8266-NodeMCU的IP

  if (SPIFFS.begin()) {                     // 启动闪存文件系统
    Serial.println("SPIFFS Started.");
  } else {
    Serial.println("SPIFFS Failed to Start.");
  }

  esp8266_server.on("/ctrl.html", HTTP_POST, ctrl);
  esp8266_server.on("/index.html", HTTP_POST, index_p);
  esp8266_server.on("/pushup.html", HTTP_POST, pushup);

  esp8266_server.on("/PUc", HTTP_POST, PUcln);
  esp8266_server.on("/PU", HTTP_POST, PUcnt);
  esp8266_server.on("/readPU", readPU);
  esp8266_server.on("/play", HTTP_POST, play);
  esp8266_server.onNotFound(handleUserRequet);      // 告知系统如何处理用户请求

  esp8266_server.begin();                           // 启动网站服务
  Serial.println("HTTP server started");
  esp8266_server.collectHeaders(headerKeys, sizeof(headerKeys) / sizeof(headerKeys[0]));
}

void loop(void) {
  esp8266_server.handleClient();                    // 处理用户请求
  if (wifiMulti.run() != WL_CONNECTED)
  {
    Serial.println("断开连接，重启中……");
    system_restart();
  }
}


void handleUserRequet() {

  // 获取用户请求网址信息
  String webAddress = esp8266_server.uri();

  // 通过handleFileRead函数处处理用户访问
  bool fileReadOK = handleFileRead(webAddress);

  // 如果在SPIFFS无法找到用户访问的资源，则回复404 (Not Found)
  if (!fileReadOK) {
    esp8266_server.send(404, "text/plain", "404 Not Found\n Please Go To \index");
  }
}
void pushup() {
  String act = esp8266_server.arg("act");
  switch (str_num(act))
  {
    case 1: myse.runActionGroup(28, 1);
    case 2: myse.runActionGroup(29, 1);
    case 3: myse.runActionGroup(30, 1);
  }
  if (act == "0")
  {
    cnt++;
    myse.runActionGroup(29, 1);
  }
  esp8266_server.send(200);
}
void ctrl() {
  String moveact = esp8266_server.arg("move");
  String group = esp8266_server.arg("group");
  if (group)
  {
    int tmp = str_num(group);
    myse.runActionGroup(tmp, 1);
  }
  esp8266_server.send(200);
}
void index_p() {
  String act = esp8266_server.arg("act");
  switch (str_num(act))
  {
    case 1: myse.runActionGroup(25, 1);//准备
    case 2: myse.runActionGroup(7, 1);//俯卧撑
    case 3: myse.runActionGroup(5, 1);//前滚翻
    case 4: myse.runActionGroup(6, 1);//后滚翻
    case 5: myse.runActionGroup(26, 1);//蹲起
    case 6: myse.runActionGroup(27, 1);//拉伸
  }
  esp8266_server.send(200);
}
void readPU() {
  String tmp = String(cnt);
  esp8266_server.send(200, "text/plain", tmp);
}
void PUcnt() {
  cnt++;
  esp8266_server.send(200);
}
void PUcln() {
  cnt = 0;
  esp8266_server.send(200, "text/plain", "Success");
}
void play()
{
  String act = esp8266_server.arg("act");
  delay(2000);
  switch (str_num(act))
  {
    case 1: myse.runActionGroup(18, 1);//小苹果
    case 2: myse.runActionGroup(17, 1);//江南STYLE
    case 3: myse.runActionGroup(20, 1); //倍爽
  }
  esp8266_server.send(200);
}
bool handleFileRead(String path) {            //处理浏览器HTTP访问

  if (path.endsWith("/")) {                   // 如果访问地址以"/"为结尾
    path = "/index.html";                     // 则将访问地址修改为/index.html便于SPIFFS访问
  }
  String contentType = getContentType(path);  // 获取文件类型

  if (SPIFFS.exists(path)) {                     // 如果访问的文件可以在SPIFFS中找到
    File file = SPIFFS.open(path, "r");          // 则尝试打开该文件
    esp8266_server.streamFile(file, contentType);// 并且将该文件返回给浏览器
    file.close();                                // 并且关闭文件
    return true;                                 // 返回true
  }
  return false;                                  // 如果文件未找到，则返回false
}
// 获取文件类型
String getContentType(String filename) {
  if (filename.endsWith(".htm")) return "text/html";
  else if (filename.endsWith(".html")) return "text/html";
  else if (filename.endsWith(".css")) return "text/css";
  else if (filename.endsWith(".js")) return "application/javascript";
  else if (filename.endsWith(".png")) return "image/png";
  else if (filename.endsWith(".gif")) return "image/gif";
  else if (filename.endsWith(".jpg")) return "image/jpeg";
  else if (filename.endsWith(".ico")) return "image/x-icon";
  else if (filename.endsWith(".xml")) return "text/xml";
  else if (filename.endsWith(".pdf")) return "application/x-pdf";
  else if (filename.endsWith(".zip")) return "application/x-zip";
  else if (filename.endsWith(".gz")) return "application/x-gzip";
  return "text/plain";
}

int str_num(String str)
{
  int ans = 0, tmp = 1;
  for (int i = str.length() - 1; i >= 0; i--)
  {
    ans += (str[i] - '0') * tmp;
    tmp *= 10;
  }
  return ans;
}
