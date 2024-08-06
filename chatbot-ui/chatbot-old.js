const se_config = {
  api: "http://localhost",
  type: "SAMPLE" // LIVE: Use LIVE URL, SAMPLE: Use dataset from sample-response.js
};
var se_cb_uid = 0; // userID


$(document).ready(function () {

  // handle error response
  function errorHandle(text) {
    $(".se-error-message").text(text);
    $(".se-error-message-block").addClass("se-active");
  }

  function formatResponse(data){
    

  }

  // handle API requests
  async function request(req) {
    try {
      if (se_config.type == "LIVE") {
        const url = se_config.api + req.endpoint;
        const options = {
          method: req.type,
          headers: { "Content-Type": "application/json" },
        };
        options.body = req.body;
        const response = await fetch(url, options);
        if (!response.ok) {
          errorHandle(`Error: ${response.statusText}`);
        }
        var data = await response.json();
      } else {
        var data = sampleDataset[req.endpoint];
      }

      if (req.endpoint == "/welcome") {

        let child_html = "";
        data.options.forEach((option) => {
          let body = JSON.stringify({
            "user_id": se_cb_uid,
            "selected_category": option.value
          });

          child_html += `<div class="se-api-request" data-endpoint="/select-category" data-type="POST" data-body='${body}'>${option.text}</div>
                    `;
        });

        let html = `<div class="se-incoming">
                      <div class="se-bubble">
                      ${data.message} 
                      <br>
                      ${child_html}
                      </div>
                    </div>
                    `;
        return html;

      } else if (req.endpoint == "/select-category") {

        let child_html = "";
        selected_category = JSON.parse(req.body).selected_category || "";
        data.options.forEach((option) => {
          let body = JSON.stringify({
            "user_id": se_cb_uid,
            "selected_category": selected_category,
            "selected_sub_category": option
          });

          child_html += `<div class="se-api-request" data-endpoint="/select-sub-category" data-type="POST" data-body='${body}'>${option}</div>
                    `;
        });

        let html = `<div class="se-incoming">
                      <div class="se-bubble">
                      ${data.message} 
                      <br>
                      ${child_html}
                      </div>
                    </div>
                    `;
        html += `<div class="se-outgoing">
                      <div class="se-bubble">
                      ${req.outgoingText} 
                      </div>
                    </div>
                    `;
        return html;

      } else if (req.endpoint == "/select-sub-category") {

        let child_html = "";
        selected_category = JSON.parse(req.body).selected_category || "";
        data.products.forEach((product) => {
          child_html += `<a href="${product.url}" target="_blank">${product.title} - ${product.price}</a> <br><br>`;
        });

        let html = `<div class="se-incoming">
                      <div class="se-bubble">
                      ${data.message} 
                      <br>
                      ${child_html}
                      </div>
                    </div>
                    `;
        html += `<div class="se-outgoing">
                      <div class="se-bubble">
                      ${req.outgoingText} 
                      </div>
                    </div>
                    `;
        return html;

      }else if (req.endpoint == "/query") {

        let child_html = "";
        data.options.forEach((option) => {
          if(typeof option === "object"){
            child_html += `<a href="${product.url}" target="_blank">${product.title} - ${product.price}</a> <br><br>`;
          }else if(typeof option === "string"){
            child_html += `<a href="${product.url}" target="_blank">${product.title} - ${product.price}</a> <br><br>`;
          }
        });

        let html = `<div class="se-incoming">
                      <div class="se-bubble">
                      ${data.message} 
                      </div>
                    </div>
                    `;
        html += `<div class="se-outgoing">
                      <div class="se-bubble">
                      ${req.outgoingText} 
                      </div>
                    </div>
                    `;
        return html;

      }else{
        errorHandle(`Error: Invalid input.`);
      }
    } catch (error) {
      errorHandle(`Error: ${error}`);
      return null;
    }
  }

  // back to main
  $(document).on("click", ".se-back", function () {
    $(".se-chats").addClass("se-active");
    $(".se-chatbox").removeClass("se-active");
  });

  // toggle chat launcher
  $(document).on("click", ".se-chat-button", function () {
    $("#se-chatbot-container").toggleClass("se-active");
  });

  // close error popup
  $(".se-error-message-close").click(function () {
    $(".se-error-message").text("");
    $(".se-error-message-block").removeClass("se-active");
  });

  // Start new chat
  $(document).on("click", ".se-new-chat", async function () {

    // Request API
    let html = await request({
      endpoint: "/welcome", // API endpoint
      type: "POST", // API method
      body: JSON.stringify({ user_id: se_cb_uid }), // API body
    })

    // Display response
    $(".se-middle-chats").html(html);

    // switch view
    $(".se-chats").removeClass("se-active");
    $(".se-chatbox").addClass("se-active");
  });


  // Call API from chat response
  $(document).on("click", ".se-api-request", async function () {

    let html = await request({
      endpoint: $(this).attr("data-endpoint"),
      type: $(this).attr("data-type"),
      body: $(this).attr("data-body"),
      outgoingText: $(this).text() // display user's input
    })

    $(".se-middle-chats").prepend(html);

  });


  // submit user's query
  $(document).on("click", ".se-submit-button", async function () {

    var query = $(".se-input").val();
    if(!query) { return false; }

    let html = await request({
      endpoint: "/query",
      type: "POST",
      body: JSON.stringify({ user_id: se_cb_uid, query: query }),
      outgoingText: query
    })

    $(".se-middle-chats").prepend(html);
    $(".se-input").val("");
  });

  // submit user's query by press Enter 
  $(document).on("keydown", ".se-input", async function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      $(".se-submit-button").click();
    }
  });

  // end of ready state
});
