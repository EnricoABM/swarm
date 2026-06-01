function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheets()[0];

  var data = JSON.parse(e.postData.contents);
  var now = new Date();
  

  sheet.appendRow([
    new Date(),
    data.event,
    data.status
  ]);

    MailApp.sendEmail({
    to: "email@teste.com",
    subject: "Alerta de Evento na Residência",
    htmlBody: `
      <h2>Evento</h2>

      <p><b>Evento:</b> ${data.event}</p>
      <p><b>Status:</b> ${data.status}</p>
      <p><b>Data:</b> ${now}</p>
    `
  });

  return ContentService
    .createTextOutput("OK")
    .setMimeType(ContentService.MimeType.TEXT);

  return ContentService
    .createTextOutput("OK")
    .setMimeType(ContentService.MimeType.TEXT);
}
