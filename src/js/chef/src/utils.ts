import { mande } from "mande";
import { API_URL } from "./constants";
import type { ServerErrorResponse } from "./types";
import type { QVueGlobals } from "quasar";

export function deepCopy(obj: object) {
  return JSON.parse(JSON.stringify(obj));
}

export function replaceUnicode(value: string) {
  // search without special czech chars
  return value
    .replaceAll("ě", "e")
    .replaceAll("š", "s")
    .replaceAll("č", "c")
    .replaceAll("ř", "r")
    .replaceAll("ž", "z")
    .replaceAll("ý", "y")
    .replaceAll("á", "a")
    .replaceAll("é", "e")
    .replaceAll("í", "i")
    .replaceAll("ů", "u")
    .replaceAll("ú", "u")
    .replaceAll("ť", "t")
    .replaceAll("ď", "d")
    .replaceAll("ó", "o")
    .replaceAll("ň", "n");
}

export function generateUUID() {
  // Generate random hexadecimal digits
  var digits = "0123456789abcdef";
  var n = digits.length;

  // Generate random hexadecimal digits and concatenate them to form the UUID
  var uuid = "";
  for (var i = 0; i < 32; i++) {
    uuid += digits[Math.floor(Math.random() * n)];
  }

  // Add hyphens to the UUID to separate it into groups
  uuid =
    uuid.substr(0, 8) +
    "-" +
    uuid.substr(8, 4) +
    "-" +
    uuid.substr(12, 4) +
    "-" +
    uuid.substr(16, 4) +
    "-" +
    uuid.substr(20, 12);

  return uuid;
}

type ServerInfo = {
  version: string;
};

export async function getServerInfo() {
  const info = mande(API_URL);
  return await info.get<ServerInfo>("/info");
}

export function catchError(e: unknown, $q: QVueGlobals) {
  const err = e as ServerErrorResponse;
  if (!err?.body?.detail) {
    $q.notify({
      color: "negative",
      message: "Unexpected error",
    });
    return
  }

  for (const detail of err.body.detail) {
    $q.notify({
      color: "negative",
      message: `${detail.msg}, input: ${detail.input}`,
    });
  }
  throw e;
}
