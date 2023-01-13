document.getElementById("submit").onclick = function () {
  StartScan();
};
function StartScan() {
  var file = document.getElementById("image_file").files;
  var filename = document.getElementById("image_file").value;
  if (file.length == 0) {
    alert("Upload Image terlebih dahulu");
  } else {
    var namafile = filename.replace(/^.*[\\\/]/, '');
    extension = filename.split(".").pop();
    var datetime = Date(Date.now());
    a = datetime.toString();
    if (extension == "png" || extension == "jpg" || extension == "jpeg") {
      Tesseract.recognize(file[0], "eng", {
        logger: (m) => console.log(m),
      }).then(({ data: { text } }) => {
        console.log(text);
        console.log(namafile);
        console.log(a);
        console.log(extension);
        //ngirim ke backend
        hasil = {"text" : text,
          "nama" : namafile,
          "extensi" : extension,
          "dateTime" : a
        }
        let option = {
          method: 'POST',
          headers: {'Content-Type': 'application/json;charset=utf-8'},
          body: JSON.stringify(hasil)
        }
        let response = fetch('/extract_text',option)
        response.then(res => res.json()).then(d => {
          console.log(d)
        })
        // var dict ={"text" : text};
        // endpoint = '/extract_text';
        // $.ajax({
        //   type: "POST",
        //   url: endpoint,
        //   data: dict,
        //   contentType: false,
        //   cache: false,
        //   processData: false,
        //   success: function (text) {
        //     alert(text);
        //   }
        // });
        if (text == "") {
          alert("Tidak dapat menemukan text");
        }
        document.getElementById("result").value = text;
        alert("Scan berhasil");
      });
    } else {
      alert("Tidak dapat memindai Image berformat " + extension);
    }
  }
  //var formData = new FormData();
  //var endpoint = '/api/v1/extract_text';
  //formData.append('image', file[0])
}

document.querySelector(".converted-text--container__svg").onclick =
  function () {
    document.querySelector("textarea").select();
    document.execCommand("copy");
  };

$("textarea").keyup(function () {
  var characterCount = $(this).val().length,
    current = $("#current"),
    maximum = $("#maximum"),
    theCount = $("#the-count");

  current.text(characterCount);

  /*This isn't entirely necessary, just playin around*/
  if (characterCount < 100) {
    current.css("color", "#666");
  }
  if (characterCount > 100 && characterCount < 200) {
    current.css("color", "#6d5555");
  }
  if (characterCount > 200 && characterCount < 400) {
    current.css("color", "#793535");
  }
  if (characterCount > 400 && characterCount < 620) {
    current.css("color", "#841c1c");
  }
  if (characterCount > 620 && characterCount < 939) {
    current.css("color", "#8f0001");
  }

  if (characterCount >= 1000) {
    maximum.css("color", "#8f0001");
    current.css("color", "#8f0001");
    theCount.css("font-weight", "bold");
  } else {
    maximum.css("color", "#666");
    theCount.css("font-weight", "normal");
  }
});
