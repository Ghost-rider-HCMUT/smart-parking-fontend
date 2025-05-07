#include <Wire.h>
#include <Servo.h>
#include <SPI.h>
#include <MFRC522.h> // thu vien "RFID"
Servo servov;
Servo servor;
#define CBV A0
#define CBR A1
#define CB1 A2
#define CB2 A3
#define CB3 A4
#define COI A5
#define D1  4
#define D2  3
#define D3  2
#define SAI 0
#define DUNG  1
#define BAT HIGH
#define TAT LOW
#define SS_PIN_V  10
#define RST_PIN_V 8
#define SS_PIN_R  9
#define RST_PIN_R 7
#define minr  10
#define maxr  100
#define minv  10
#define maxv  100
int find_rfid = 0;
int RFID = 0;
MFRC522 mfrc522V(SS_PIN_V, RST_PIN_V);
MFRC522 mfrc522R(SS_PIN_R, RST_PIN_R);
unsigned long uidDec, uidDecTemp; // hien thi so UID dang thap phan
byte bCounter, readBit;
unsigned long ticketNumber;
int vr = 0, index = 0, doc_bien = 0;
int i = 0, tt = 0, tt2 = 0;
int lan = 0, dong_mo = 0, cp = 0, so_xe = 0, vtri = 0;
String kqv = "", kqr = "";
String status = "";
int mode = 0, dk_vao = 0, dk_ra = 0, lan2 = 0;
int tt_vao = 0, tt_ra = 0, dc_ra = 0;
String dataa = "";
char *token1, *token2, *token3, *token4;
char tama[30];
String mang_bien[10];
unsigned long mang_id[10];
unsigned long int time_vao = 0, time_ra = 0, time_gui = 0, time_cho = 0, time_docrf = 0;
//****************************************************************************************//
void setup() {
  Serial.begin(9600);
  pinMode(CBV, INPUT_PULLUP);
  pinMode(CBR, INPUT_PULLUP);
  pinMode(CB1, INPUT_PULLUP);
  pinMode(CB2, INPUT_PULLUP);
  pinMode(CB3, INPUT_PULLUP);
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(COI, OUTPUT);
  digitalWrite(D1, TAT);
  digitalWrite(D2, TAT);
  digitalWrite(D3, TAT);
  digitalWrite(COI, TAT);
  servov.attach(6);
  servor.attach(5);
  servov.write(minv);
  servor.write(minr);
  SPI.begin();
  delay(1000);
}
//****************************************************************************************//
void loop() {
  //  Serial.println(digitalRead(CB1));
  if (millis() - time_docrf <= 500) {
    doc_ra();
  }
  else if (millis() - time_docrf <= 1000) {
    doc_vao();
  }
  else {
    time_docrf = millis();
  }
  if (mode == 0) {
    Auto();
  }
  else {
    Man();
  }
  vr = 0;
  if (digitalRead(CB1) == 0) {
    digitalWrite(D1, BAT);
  }
  else {
    digitalWrite(D1, TAT);
  }

  if (digitalRead(CB2) == 0) {
    digitalWrite(D2, BAT);
  }
  else {
    digitalWrite(D2, TAT);
  }

  if (digitalRead(CB3) == 0) {
    digitalWrite(D3, BAT);
  }
  else {
    digitalWrite(D3, TAT);
  }
  guidulieu();
}
//****************************************************************************************//
void Auto() {
 if (digitalRead(CBV) == 0) {
   if (vr == 1) {
     cp = 1;
     guidulieu2();
     cp = 0;

     unsigned long startTime = millis();
     while (millis() - startTime < 5000) {
       serialEvent();
       if (status != "") {
         Serial.print("STATUS=");
         Serial.println(status);
         break;
       }
     }

     if (status == "OK") {
       // Mở cổng ngay lập tức
       mov();

       // Đợi cho đến khi xe đi qua (CBV = 1)
       startTime = millis();
       while (digitalRead(CBV) == 0) {
         if (millis() - startTime > 10000) {  // Timeout 10 giây
           break;
         }

         serialEvent();
         guidulieu();
         delay(100);  
       }

       // Đóng cổng sau khi xe đi qua
       guidulieu2();
       delay(500);
       dongv();
     } 
     doc_bien = 0;
     vr = 0;
     status = "";
   }
 }

 if (digitalRead(CBR) == 0) {
   if (vr == 2) {              // Trạng thái sẵn sàng xử lý xe ra
     cp = 1;
     guidulieu2();             // Gửi tín hiệu bắt đầu xử lý
     cp = 0;

     // Đợi phản hồi từ Backend
     unsigned long startTime = millis();
     while (millis() - startTime < 5000) {
       serialEvent();          // Đọc phản hồi từ Backend
       if (status != "") {
         Serial.print("STATUS=");
         Serial.println(status);
         break;
       }
     }

     // Phản hồi OK -> Cho phép xe ra
     if (status == "OK") {
       mor();                  // Mở cổng
       dc_ra = 1;
       guidulieu2();           // Gửi trạng thái xác nhận đã mở
       dc_ra = 0;

       // Đợi xe ra khỏi làn (CBR == 1)
       while (digitalRead(CBR) == 0) {
         serialEvent();
       }

       delay(500);
       dongr();                // Đóng cổng sau khi xe ra
     }
     else {
       dc_ra = 2;
       guidulieu2();           // Gửi trạng thái từ chối
       dc_ra = 0;
     }

     // Reset biến
     uidDec = "";
     status = "";
     vr = 0;
   }
 }


//   if (digitalRead(CBR) == 0) {
//     if (vr == 2) {
//       cp = 1;
//       guidulieu2();
//       cp = 0;
//
//       while (doc_bien == 0) {
//         serialEvent();
//         guidulieu();
//       }
//       doc_bien = 0;
//       vr = 0;
//
//       for (int i = 0; i <= 2; i++) {
//         if (uidDec == mang_id[i])  vtri = i;
//       }
//       if (kqr == mang_bien[vtri]) {
//         mor();
//         so_xe--;
//         dc_ra = 1;
//         guidulieu2();
//         dc_ra = 0;
//         while (digitalRead(CBR) == 0) {
//           serialEvent();
//           guidulieu();
//         }
//         delay(500);
//         dongr();
//       }
//       else{
//         dc_ra = 2;
//         guidulieu2();
//         dc_ra = 0;
//       }
//     }
//   }
}
//****************************************************************************************//

//****************************************************************************************//
void Man() {
  if (dk_vao == 0) {
    dongv();
  }
  else            {
    mov();
  }
  if (dk_ra == 0)  dongr();
  else            mor();
}
//****************************************************************************************//
void serialEvent() {
  while (Serial.available()) {
    dataa = Serial.readStringUntil('\n');  // Đọc đến ký tự xuống dòng
    dataa.trim();  // Loại bỏ khoảng trắng và ký tự xuống dòng

    // Debug để kiểm tra dữ liệu nhận được
    Serial.print("Received: ");
    Serial.println(dataa);

    int delimiterIndex = dataa.indexOf('|');
    if (delimiterIndex != -1) {
      String command = dataa.substring(0, delimiterIndex);
      String value = dataa.substring(delimiterIndex + 1);

      if (command == "a") mode = value.toInt();
      else if (command == "b") dk_vao = value.toInt();
      else if (command == "c") dk_ra = value.toInt();
      else if (command == "d") {
        status = value;
        Serial.print("Status updated: ");
        Serial.println(status);
      }
    }
  }
}
//****************************************************************************************//
void mov() {
  if (tt == 0) {
    for (i = minv; i <= maxv; i++) {
      servov.write(i);
      delay(3);
    }
  }
  tt_vao = 1;
  tt = 1;
}
//---------------------------------------------------------------
void dongv() {
  if (tt == 1) {
    for (i = maxv; i >= minv; i--) {
      while (digitalRead(CBV) == 0) {
      }
      servov.write(i);
      delay(10);
    }
    tt_vao = 0;
    tt = 0;
  }
}
//---------------------------------------------------------------
//****************************************************************************************//
void mor() {
  if (tt2 == 0) {
    for (i = minr; i <= maxr; i++) {
      servor.write(i);
      delay(3);
    }
  }
  tt_ra = 1;
  tt2 = 1;
}
//---------------------------------------------------------------
void dongr() {
  if (tt2 == 1) {
    for (i = maxr; i >= minr; i--) {
      while (digitalRead(CBR) == 0) {
      }
      servor.write(i);
      delay(10);
    }
    tt_ra = 0;
    tt2 = 0;
  }
}
//****************************************************************************************//
void guidulieu() {
  if (millis() - time_gui >= 200) {
    Serial.print(mode);
    Serial.print("|");
    Serial.print(tt_vao);
    Serial.print("|");
    Serial.print(tt_ra);
    Serial.print("|");
    Serial.print(cp);
    Serial.print("|");
    Serial.print(vr);
    Serial.print("|");
    Serial.print(dc_ra);
    Serial.print("|");
    Serial.println(so_xe);
    time_gui = millis();
  }
}
//****************************************************************************************//
void guidulieu2() {
  Serial.print(mode);
  Serial.print("|");
  Serial.print(tt_vao);
  Serial.print("|");
  Serial.print(tt_ra);
  Serial.print("|");
  Serial.print(cp);
  Serial.print("|");
  Serial.print(vr);
  Serial.print("|");
  Serial.print(dc_ra);
  Serial.print("|");
  Serial.println(so_xe);
  time_gui = millis();
}
//****************************************************************************************//
void doc_vao() {
  mfrc522V.PCD_Init();
  if ( ! mfrc522V.PICC_IsNewCardPresent()) {
    find_rfid = 1;
    lan = 0;
  }
  else  find_rfid = 0;
  if ( ! mfrc522V.PICC_ReadCardSerial()) {
    find_rfid = 1;
    lan = 0;
  }
  else  find_rfid = 0;

  if (find_rfid == 0) {
    vr = 1;
    uidDec = 0;
    for (byte i = 0; i < mfrc522V.uid.size; i++) {
      uidDecTemp = mfrc522V.uid.uidByte[i];
      uidDec = uidDec * 256 + uidDecTemp;
    }

    Serial.print("RFID=");
    Serial.println(uidDec);
    digitalWrite(COI, HIGH);
    delay(200);
    digitalWrite(COI, LOW);
    delay(200);
    digitalWrite(COI, HIGH);
    delay(200);
    digitalWrite(COI, LOW);
  }
}
//****************************************************************************************//
void doc_ra() {
  mfrc522R.PCD_Init();
  // Tim the moi
  if ( ! mfrc522R.PICC_IsNewCardPresent()) {
    //return;
    find_rfid = 1;
    lan = 0;
  }
  else  find_rfid = 0;
  // Doc the
  if ( ! mfrc522R.PICC_ReadCardSerial()) {
    //return;
    find_rfid = 1;
    lan = 0;
  }
  else  find_rfid = 0;

  if (find_rfid == 0) {
    vr = 2;
    uidDec = 0;
    for (byte i = 0; i < mfrc522R.uid.size; i++) {
      uidDecTemp = mfrc522R.uid.uidByte[i];
      uidDec = uidDec * 256 + uidDecTemp;
    }

    Serial.print("RFID=");
    Serial.println(uidDec);
    digitalWrite(COI, HIGH);
    delay(200);
    digitalWrite(COI, LOW);
    delay(200);
    digitalWrite(COI, HIGH);
    delay(200);
    digitalWrite(COI, LOW);
  }
}