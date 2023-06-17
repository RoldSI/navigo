var express = require("express");
var app = express();

app.use(express.static("dist/frontend"));
app.get ("/", function (reg, res) {
  res.redirect("/");
});
app.listen (4200);
