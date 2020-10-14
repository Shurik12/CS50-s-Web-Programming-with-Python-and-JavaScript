document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', function() {
    history.pushState({'mailbox': 'inbox'}, null, '/emails/inbox');
    load_mailbox('inbox');
  });
  document.querySelector('#sent').addEventListener('click', function() {
    history.pushState({'mailbox': 'sent'}, null, '/emails/sent');
    load_mailbox('sent');
  });
  document.querySelector('#archived').addEventListener('click', function() {
    history.pushState({'mailbox': 'archived'}, null, '/emails/archived');
    load_mailbox('archived');
  });
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  history.pushState({'mailbox': 'inbox'}, null, '/emails/inbox');
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // request get to ...
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((element) => {
        if (mailbox != "sent") {
          sender_recipients = element.sender;
        } else {
          sender_recipients = element.recipients;
        }
        if (mailbox == "inbox") {
          console.log("inbox");
          console.log(element.subject);
          if (element.read) is_read = "read";
          else is_read = "";
        } else is_read = "";
        var item = document.createElement("div");
        item.className = `message ${is_read} my-1 items`;
        item.innerHTML = 
        `<div class="Row" id="item-${element.id}">
            <div class="Column" style="font-weight:600;">${sender_recipients}</div>
            <div class="Column">${element.subject}</div>
            <div class="Column">${element.timestamp}</div>
        </div>`;
        document.querySelector("#emails-view").appendChild(item);
        item.addEventListener("click", () => {
          show_mail(element.id, mailbox);
        });
      });
      // Push state to URL.
      // document.title = mailbox;
      // history.pushState({'mailbox': mailbox}, null, `/emails/${mailbox}`);
      // console.log(history)
    });
}

// Update text on popping state.
window.onpopstate = function(event) {
    load_mailbox(event.state.mailbox);
}

function show_mail(id, mailbox) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      // console.log(email);
      document.querySelector("#emails-view").innerHTML = "";
      var item = document.createElement("div");
      item.className = `message`;
      item.innerHTML = `<div class="message-body" style="{background:gray}">
                          <br><b> From: </b> ${email.sender}
                          <br><b> To: </b> ${email.recipients}
                          <br><b> Subject: </b> ${email.subject}
                          <br><b> Timestamp: </b> ${email.timestamp}
                        </div>`;
      document.querySelector("#emails-view").appendChild(item);
      if (mailbox == "sent") return;
      let archive = document.createElement("btn");
      archive.className = `btn btn-outline-info my-2`;
      archive.addEventListener("click", () => {
        toggle_archive(id, email.archived);
        if (archive.innerText == "Archive") archive.innerText = "Unarchive";
        else archive.innerText = "Archive";
      });
      if (!email.archived) archive.textContent = "Archive";
      else archive.textContent = "Unarchive";
      document.querySelector("#emails-view").appendChild(archive);

      let reply = document.createElement("btn");
      reply.className = `btn btn-outline-success m-2`;
      reply.textContent = "Reply";
      reply.addEventListener("click", () => {
        reply_mail(email.sender, email.subject, email.body, email.timestamp);
      });
      document.querySelector("#emails-view").appendChild(reply);

      var item = document.createElement("div");
      item.className = `message`;
      item.innerHTML = `<div class="message-body">
                          ${email.body}
                        </div>`;
      document.querySelector("#emails-view").appendChild(item);

      make_read(id);
    });
}

function toggle_archive(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    }),
  });
}

function make_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function reply_mail(sender, subject, body, timestamp) {
  compose_email();
  if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;

  pre_fill = `On ${timestamp} ${sender} wrote:\n${body}\n`;

  document.querySelector("#compose-body").value = pre_fill;
}