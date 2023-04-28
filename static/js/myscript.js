$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var quan = this.parentNode.children[2];
  console.log(quan);
  console.log("pid=", id);
  $.ajax({
    type: "GET",
    url: "/plusCart",
    data: {
      product_id: id,
    },
    success: function (data) {
      console.log("data=", data);
      quan.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var quan = this.parentNode.children[2];
  console.log("pid=", id);

  $.ajax({
    type: "GET",
    url: "/minusCart",
    data: {
      product_id: id,
    },
    success: function (data) {
      console.log("data=", data);
      quan.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;

    if (id.quantity === 1) {
        console.log("after tapping minus button", data.quantity);
        $(".minus-cart").attr("disabled", true);
    
    }else{
      $(".minus-cart").attr("disabled", false);
      }
      }
    });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var quan = this; // remove current div object
  $.ajax({
    type: "GET",
    url: "/removeCart",
    data: {
      product_id: id,
    },
    success: function (data) {
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      quan.parentNode.parentNode.parentNode.parentNode.remove(); 
    },
  });
});

$(".plus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();
  $.ajax({
    type: "GET",
    url: "/plusWishlist",
    data: {
      product_id: id,
    },
    success: function (data) {
      window.location.href = `http://localhost:8000/product-detail/${id}`;
    },
  });
});

$(".minus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();
  $.ajax({
    type: "GET",
    url: "/minusWishlist",
    data: {
      product_id: id,
    },
    success: function (data) {
      window.location.href = `http://localhost:8000/product-detail/${id}`;
    },
  });
});

$('.otp').change(function(){
   var otp=$('.otp').val();
   console.log("OTP=",otp)

   if (otp == "{otp}"){
    console.log("Otp matched ")

    $.ajax({
      type: "POST",
      url:"/verifyEmail",
      data: {'otp':otp,
             'name':"{{name}}",
              'email':"{{email}}",
              'password1':"{{password1}}",
              'password2':"{{password2}}",
    },

      success:function(data){
        console.log("OTP Success")
        window.location.href= `http://localhost:8000/accounts/login`;
      }
    })
   } 
})