<script>

export default {
  HOST_URL: 'http://www.chef.home/rest',
  // HOST_URL: 'http://localhost:5000',
  IMAGES_URL: 'http://www.chef.home/rest/images',

  methods: {
    replaceUnicode(str) {
      // search without special czech chars
      return str
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
    },
  }
};

</script>
