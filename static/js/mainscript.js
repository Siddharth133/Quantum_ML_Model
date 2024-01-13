var marineSpeciesDescriptions = {
    'Clams': [
        "Clams are a type of marine bivalve mollusk, found in both freshwater and marine environments.",
        "They are encased in a hinged shell and are filter feeders, consuming plankton and other small organisms.",
        "Clams play an important role in the aquatic food chain and are indicators of environmental health.",
        "They are also valued as a food source, with a global market for both wild-caught and farmed clams.",
        "Overharvesting and pollution are significant threats to clam populations in various regions."
    ],
    'Corals': [
        "Corals are marine invertebrates within the class Anthozoa of the phylum Cnidaria.",
        "They typically live in compact colonies of many identical individual polyps.",
        "Corals secrete calcium carbonate to form a hard skeleton, which forms coral reefs.",
        "Reefs are important marine ecosystems, providing habitat for a diverse range of species.",
        "Coral reefs are under threat from climate change, ocean acidification, pollution, and destructive fishing practices."
    ],
    'Crabs': [
        "Crabs are decapod crustaceans of the infraorder Brachyura, known for their short projecting tail and two large claws.",
        "They are found in all the world's oceans, in fresh water, and on land.",
        "Crabs are omnivores, feeding on algae, plankton, detritus, and other small organisms.",
        "They play a significant role in the marine ecosystem as both predator and prey.",
        "Crabs are also a popular seafood, but overfishing and habitat destruction pose threats to certain species."
    ],
    'Dolphin': [
        "Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.",
        "They are known for their playful behavior, making them popular in human culture.",
        "Dolphins are carnivores, mostly eating fish and squid.",
        "Dolphin coloration varies, but they are generally gray in color with darker backs and lighter bellies.",
        "They are well known for their agility and playful behavior, making them a favorite of wildlife watchers."
    ],
    'Eel': [
        "Eels are elongated fish, ranging in length from 5 centimeters to 4 meters.",
        "Their snakelike bodies are adapted to burrowing in sand, mud, and among rocks.",
        "Most eels live in the shallow waters of the ocean and burrow into sand, mud, or amongst rocks.",
        "Eels are an important source of food for humans and are also popular in home aquariums.",
        "Some species of eel are known for their remarkable migrations, traveling large distances to breed."
    ],
    'Fish': [
        "Fish are gill-bearing aquatic craniate animals that lack limbs with digits.",
        "They form a sister group to the tunicates, together forming the olfactores."]
}
function classifyImage() {
    var formData = new FormData();
    var fileInput = document.getElementById('image-upload');
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response[0] === "Error") {
                    alert("Error: " + response[1]);
                    return;
                }

                var classificationText = "Image Classification: " + response[0];
                var imagePath = "/static/images/" + response[1].toString() + ".jpeg";
                var aboutText = document.getElementById('img-ident-about');
                 var speciesInfo = marineSpeciesDescriptions[response[0]];
                if (speciesInfo) {
                    // Join the array elements into a string, separated by line breaks.
                    aboutText.innerHTML = speciesInfo.join("<br><br>");
                } else {
                    aboutText.innerText = "No additional information available.";
                }

                document.getElementById('classification-result').innerText = classificationText;
                document.getElementById('classified-image').src = imagePath;
                document.getElementById('classified-image').alt = response[0];

                document.querySelector('.class-sec').classList.remove('invis');
                document.querySelector('.iden-sec').classList.remove('invis');
                document.querySelector('.imginf-sect').style.display = 'block';
            },
            error: function(error) {
                console.log(error);
                alert('Error: ' + error.responseText);
            }
        });
    } else {
        alert('Please select an image file to classify.');
    }
}



//function classifyImage() {
//    var formData = new FormData();
//    var fileInput = document.getElementById('FileInput');
//    if (fileInput.files.length > 0) {
//        formData.append('file', fileInput.files[0]);
//
//        $.ajax({
//            type: 'POST',
//            url: '/predict',
//            data: formData,
//            contentType: false,
//            processData: false,
//            success: function(response) {
//                // Assuming response is an object with classification and index
//                var classificationText = "Image Classification: " + result.classification;
//                var imagePath = "/static/images/" + result.index + ".jpg";
//
//                // Update the classification text
//                document.getElementById('classification-result').innerText = classificationText;
//
//                // Update the image source
//                document.getElementById('classified-image').src = imagePath;
//                document.getElementById('classified-image').alt = result.classification;
//
//                // Make sections visible
//                document.querySelector('.class-sec').classList.remove('invis');
//                document.querySelector('.iden-sec').classList.remove('invis');
//                document.querySelector('.imginf-sect').style.display = 'block';
//            },
//            error: function(error) {
//                console.log(error);
//            }
//        });
//    } else {
//        alert('Please select an image file to classify.');
//    }
//}


//
//function classifyImage() {
//    var formData = new FormData();
//    var fileInput = document.getElementById('FileInput');
//    document.querySelector('.class-sec').classList.remove('invis');
//    document.querySelector('.iden-sec').classList.remove('invis');
//    document.querySelector('.imginf-sect').style.display='block';
//    if (fileInput.files.length > 0) {
//        formData.append('file', fileInput.files[0]);
//
//        $.ajax({
//            type: 'POST',
//            url: '/predict',
//            data: formData,
//            contentType: false,
//            processData: false,
//            success: function(response) {
//                // Update the page with the response
//                document.getElementById('classification-result').innerText = "Image Classification: " + response[0];
//                document.querySelector('.class-sec').classList.remove('invis');
//            },
//            error: function(error) {
//                console.log(error);
//            }
//        });
//    } else {
//        alert('Please select an image file to classify.');
//    }
//}

//
//function classifyImage() {
//    // Add your image classification logic here
//    // Update the content in #classification-result and #image-preview
//    // document.getElementById('classification-section').style.display = 'block';
//    // document.getElementById('identification-section').style.display = 'block';
//    // document.getElementById('image-info-section').style.display = 'block';
//    // document.querySelector('.class-sec').classList.add('class-sec-pseudo');
//    document.querySelector('.class-sec').classList.remove('invis');
//    document.querySelector('.iden-sec').classList.remove('invis');
//
//
//    // document.querySelector('.class-sec').style.display='block';
//    // document.querySelector('.iden-sec').style.display='block';
//    document.querySelector('.imginf-sect').style.display='block';
//
//    // document.getElementsByClassName('class-sec').style.display='block'
//    // document.getElementsByClassName('iden-sec').style.display='block'
//    // document.getElementsByClassName('imginf-sect').style.display='block'
//
//    // document.getElementById('know-more-section').style.display = 'block';
//}

// for video slider;
const btns=document.querySelectorAll(".nav-btn");
const slids=document.querySelectorAll(".video-slide");


var sliderNav=function(manual){
    btns.forEach((btn)=>{
        btn.classList.remove("active");
    });
    slids.forEach((slide)=>{
        slide.classList.remove("active");
    });
    btns[manual].classList.add("active");
    slids[manual].classList.add("active");
}
btns.forEach((btn,i)=>{
    btn.addEventListener("click",()=>{
        sliderNav(i);
    })
});



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// // Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// chatbot
$(function() {
  var INDEX = 0;
  $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val().trim();
    if (msg == '') {
      return false;
    }

    // Send user message to the /chat route
    $.ajax({
      type: "POST",
      url: "/chat",
      data: { message: msg },
      success: function(response) {
        // Process and display the response from the chatbot
        generate_message(msg, 'self');
        generate_message(response.response, 'user');
      },
      error: function(err) {
        console.error(err);
      }
    });
  });

//$(function() {
//  var INDEX = 0;
//  $("#chat-submit").click(function(e) {
//    e.preventDefault();
//    var msg = $("#chat-input").val();
//    if(msg.trim() == ''){
//      return false;
//    }
//    generate_message(msg, 'self');
//    var buttons = [
//        {
//          name: 'Existing User',
//          value: 'existing'
//        },
//        {
//          name: 'New User',
//          value: 'new'
//        }
//      ];
//    setTimeout(function() {
//      generate_message(msg, 'user');
//    }, 1000)
//
//  })
  
  function generate_message(msg, type) {
    INDEX++;
    var str="";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
    str += "          <span class=\"msg-avatar\">";
    str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
    str += "          <\/span>";
    str += "          <div class=\"cm-msg-text\">";
    str += msg;
    str += "          <\/div>";
    str += "        <\/div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    if(type == 'self'){
     $("#chat-input").val(''); 
    }    
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
  }  
  
  function generate_button_message(msg, buttons){    
    /* Buttons should be object array 
      [
        {
          name: 'Existing User',
          value: 'existing'
        },
        {
          name: 'New User',
          value: 'new'
        }
      ]
    */
    INDEX++;
    var btn_obj = buttons.map(function(button) {
       return  "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\""+button.value+"\">"+button.name+"<\/a><\/li>";
    }).join('');
    var str="";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg user\">";
    str += "          <span class=\"msg-avatar\">";
    str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
    str += "          <\/span>";
    str += "          <div class=\"cm-msg-text\">";
    str += msg;
    str += "          <\/div>";
    str += "          <div class=\"cm-msg-button\">";
    str += "            <ul>";   
    str += btn_obj;
    str += "            <\/ul>";
    str += "          <\/div>";
    str += "        <\/div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);   
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);
    $("#chat-input").attr("disabled", true);
  }
  
  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'self');
  })
  
  $("#chat-circle").click(function() {    
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
})