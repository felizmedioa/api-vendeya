const SHEET_NAME = "Pedidos Forms";

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME) || SpreadsheetApp.getActiveSpreadsheet().insertSheet(SHEET_NAME);
    const data = JSON.parse(e.postData.contents);
    const action = data.action || "create_pedido";
    
    // Configurar cabeceras si la hoja está vacía
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["ID-Usuario", "Agencia", "Nombre-Completo", "DNI", "Telefono", "Destino", "Direccion", "ID-Pedido", "Estado", "Fecha", "Timestamp"]);
    }
    
    if (action === "create_pedido") {
      const newId = "PED-" + sheet.getLastRow(); // Usa el número de fila como secuencial único (ej. PED-1, PED-2...)
      
      sheet.appendRow([
        data.id_usuario,
        data.agencia,
        data.nombre_completo,
        data.dni,
        data.telefono,
        data.destino,
        data.direccion,
        newId,
        data.estado,
        data.fecha,
        data.timestamp
      ]);
      return ContentService.createTextOutput(JSON.stringify({ 
        status: "success", 
        message: "Pedido creado satisfactoriamente",
        id_pedido: newId
      })).setMimeType(ContentService.MimeType.JSON);
    } 
    else if (action === "update_status") {
      const pedidosIds = data.pedidos_ids || [];
      const nuevoEstado = data.nuevo_estado || "Impreso";
      
      const lastRow = sheet.getLastRow();
      if (lastRow <= 1) {
        return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "No hay pedidos para actualizar" })).setMimeType(ContentService.MimeType.JSON);
      }
      
      const range = sheet.getRange(2, 1, lastRow - 1, 11);
      const values = range.getValues();
      let updatedCount = 0;
      
      for (let i = 0; i < values.length; i++) {
        const idPedido = values[i][7]; // Col H (índice 7): ID-Pedido
        if (pedidosIds.includes(idPedido)) {
          values[i][8] = nuevoEstado; // Col I (índice 8): Estado
          updatedCount++;
        }
      }
      
      // Actualizar la hoja solo si hubieron cambios
      if (updatedCount > 0) {
        range.setValues(values);
      }
      
      return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "Pedidos actualizados", updated_count: updatedCount })).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Action not recognized" })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) {
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: [] })).setMimeType(ContentService.MimeType.JSON);
    }
    
    const idUsuario = e.parameter.id_usuario;
    if (!idUsuario) {
      return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Se requiere el parámetro id_usuario" })).setMimeType(ContentService.MimeType.JSON);
    }
    
    const lastRow = sheet.getLastRow();
    if (lastRow <= 1) {
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: [] })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Obtener los datos sin la fila de cabeceras
    const values = sheet.getRange(2, 1, lastRow - 1, 11).getValues();
    const result = [];
    
    for (let i = 0; i < values.length; i++) {
      if (values[i][0] == idUsuario) { // Col A (índice 0): ID-Usuario
        result.push({
          id_usuario: values[i][0],
          agencia: values[i][1],
          nombre_completo: values[i][2],
          dni: values[i][3],
          telefono: values[i][4],
          destino: values[i][5],
          direccion: values[i][6],
          id_pedido: values[i][7],
          estado: values[i][8],
          fecha: values[i][9],
          timestamp: values[i][10]
        });
      }
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: "success", data: result, total: result.length })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}
