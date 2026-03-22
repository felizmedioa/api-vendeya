// ============================================================================
// Google Apps Script — Registro de usuarios
// ============================================================================
// Columnas en la hoja: A = Usuario | B = Contraseña (hasheada) | C = ID único
// ============================================================================

const SHEET_NAME = "Usuarios"; // Nombre de la hoja dentro del Spreadsheet

/**
 * Genera un ID único de 12 caracteres (alfanumérico).
 */
function generateUniqueId() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let id = "";
    for (let i = 0; i < 12; i++) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
}

/**
 * Obtiene la hoja "Usuarios", o la crea si no existe con encabezados.
 */
function getOrCreateSheet() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);

    if (!sheet) {
        sheet = ss.insertSheet(SHEET_NAME);
        sheet.appendRow(["Usuario", "Contraseña", "ID"]);
    }

    return sheet;
}

/**
 * Verifica si un usuario ya existe en la hoja.
 */
function userExists(sheet, user) {
    const data = sheet.getDataRange().getValues();

    // Empezar desde fila 1 (fila 0 son encabezados)
    for (let i = 1; i < data.length; i++) {
        if (data[i][0] === user) {
            return true;
        }
    }

    return false;
}

/**
 * Verifica que el ID generado no esté duplicado.
 */
function isIdUnique(sheet, id) {
    const data = sheet.getDataRange().getValues();

    for (let i = 1; i < data.length; i++) {
        if (data[i][2] === id) {
            return false;
        }
    }

    return true;
}

/**
 * Genera un ID único que no exista en la hoja.
 */
function generateSafeUniqueId(sheet) {
    let id;
    let attempts = 0;

    do {
        id = generateUniqueId();
        attempts++;
        if (attempts > 100) {
            throw new Error("No se pudo generar un ID único después de 100 intentos");
        }
    } while (!isIdUnique(sheet, id));

    return id;
}

// ============================================================================
// Handler principal — recibe POST del backend
// ============================================================================

function doPost(e) {
    try {
        const body = JSON.parse(e.postData.contents);
        const action = body.action || "register"; // Acción por defecto

        // --- Flujo de Actualización de Contraseña ---
        if (action === "update_password") {
            const userId = body.userId;
            const newPassword = body.newPassword;

            if (!userId || !newPassword) {
                return ContentService
                    .createTextOutput(JSON.stringify({
                        status: "error",
                        message: "Faltan campos requeridos (userId, newPassword)"
                    }))
                    .setMimeType(ContentService.MimeType.JSON);
            }

            const sheet = getOrCreateSheet();
            const data = sheet.getDataRange().getValues();

            // Buscar por Token (ID) en la columna C (índice 2)
            for (let i = 1; i < data.length; i++) {
                if (data[i][2] === userId) {
                    // Actualizar la contraseña directamente con el nuevo hash
                    sheet.getRange(i + 1, 2).setValue(newPassword);
                        
                    return ContentService
                        .createTextOutput(JSON.stringify({
                            status: "success",
                            message: "contraseña modificada exitosamente"
                        }))
                        .setMimeType(ContentService.MimeType.JSON);
                }
            }

            return ContentService
                .createTextOutput(JSON.stringify({
                    status: "error",
                    message: "Usuario no encontrado con el userId proporcionado"
                }))
                .setMimeType(ContentService.MimeType.JSON);
        }

        // --- Flujo normal de registro ---
        const user = body.user;
        const password = body.password;

        // Validar campos requeridos
        if (!user || !password) {
            return ContentService
                .createTextOutput(JSON.stringify({
                    status: "error",
                    message: "Faltan campos requeridos (user, password)"
                }))
                .setMimeType(ContentService.MimeType.JSON);
        }

        const sheet = getOrCreateSheet();

        // Verificar si el usuario ya existe
        if (userExists(sheet, user)) {
            return ContentService
                .createTextOutput(JSON.stringify({
                    status: "error",
                    message: "El usuario ya existe"
                }))
                .setMimeType(ContentService.MimeType.JSON);
        }

        // Generar ID único y agregar fila
        const uniqueId = generateSafeUniqueId(sheet);
        sheet.appendRow([user, password, uniqueId]);

        return ContentService
            .createTextOutput(JSON.stringify({
                status: "success",
                message: "Usuario registrado correctamente",
                userId: uniqueId
            }))
            .setMimeType(ContentService.MimeType.JSON);

    } catch (error) {
        return ContentService
            .createTextOutput(JSON.stringify({
                status: "error",
                message: "Error interno: " + error.message
            }))
            .setMimeType(ContentService.MimeType.JSON);
    }
}

function doGet(e) {
    try {
        const action = e.parameter.action;

        if (action === "login") {
            const user = e.parameter.user;
            if (!user) {
                return ContentService.createTextOutput(JSON.stringify({
                    status: "error", message: "Falta el parámetro user"
                })).setMimeType(ContentService.MimeType.JSON);
            }

            const sheet = getOrCreateSheet();
            const data = sheet.getDataRange().getValues();

            for (let i = 1; i < data.length; i++) {
                if (data[i][0] === user) {
                    return ContentService.createTextOutput(JSON.stringify({
                        status: "success",
                        password: data[i][1],
                        userId: data[i][2]
                    })).setMimeType(ContentService.MimeType.JSON);
                }
            }

            return ContentService.createTextOutput(JSON.stringify({
                status: "error", message: "Usuario no encontrado"
            })).setMimeType(ContentService.MimeType.JSON);
        }

        return ContentService.createTextOutput(JSON.stringify({
            status: "ok", message: "Script de registro activo"
        })).setMimeType(ContentService.MimeType.JSON);

    } catch (error) {
        return ContentService.createTextOutput(JSON.stringify({
            status: "error", message: "Error interno: " + error.message
        })).setMimeType(ContentService.MimeType.JSON);
    }
}

