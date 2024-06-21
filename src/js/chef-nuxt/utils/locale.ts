
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
    .replaceAll("ň", "n")
}