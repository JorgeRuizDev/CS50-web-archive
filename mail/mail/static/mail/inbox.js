document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(default_values) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#show-email-view').style.display = 'none';

    document.title = 'Compose Email';

    // Get the composition fields
    let form = document.getElementById('compose-form');

    let recipient = document.querySelector('#compose-recipients');
    let subject = document.querySelector('#compose-subject');
    let body = document.querySelector('#compose-body');

    // Assign values:
    recipient.value = default_values["recipient"] === undefined ? "" : default_values["recipient"];
    subject.value = default_values["subject"] === undefined ? "" : default_values["subject"];
    body.value = default_values["body"] === undefined ? "" : default_values["body"];

    let button = document.querySelector('#submit-compose');


    // Invisible Help + feedback
    let mouse_over_help = document.querySelector("#compose_recipients_help");
    let recipient_feedback = document.querySelector('#invalid_compose_recipients');
    recipient_feedback.style.display = "none";
    mouse_over_help.style.display = "none";
    recipient.classList.remove("is-valid", "is-invalid");


    // Clear out the ERROR Flags
    recipient_feedback.style.display = "none";

    // Disable the submit button
    button.disabled = true;

    // Help on hover listener:
    recipient.onmouseover = () => {
        mouse_over_help.style.display = "block";
    };

    //On keyup listeners
    recipient.onkeyup = validate_form;
    body.onkeyup = validate_form;
    subject.onkeyup = validate_form;

    function validate_form() {
        button.disabled = !(recipient.value.length > 0
            && subject.value.length > 0
            && body.value.length > 0);
    }

    form.onsubmit = () => {


        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipient.value,
                subject: subject.value,
                body: body.value
            })
        })
            .then(response => response.json())
            .then(result => {

                if (result["error"]) {
                    recipient.classList.add("is-invalid");
                    recipient_feedback.innerHTML = result["error"];
                    recipient_feedback.style.display = "block";
                } else {
                    // Clear out the composition fields
                    recipient.value = '';
                    subject.value = '';
                    body.value = '';

                    load_mailbox("sent");
                }
            });
        return false;
    };

}


function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#show-email-view').style.display = 'none';

    let title = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

    // Show the mailbox name
    document.querySelector('#emails-view-header').innerHTML = `<h3>${title}</h3>`;

    document.title = title;

    // Clear the previous list
    document.querySelector("#emails-view-table").innerHTML = `<tr> 
        <th></th>
        <th>Sender:</th>
        <th>Subject:</th>
        <th></th>
    </tr>`;

    // Query the mailbox

    fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => Object.entries(emails))
        .then(emails => {
                emails.forEach(
                    mail => {
                        let element = document.createElement('tr');


                        if (mail[1]["read"] === true)
                            element.className += "read";


                        element.innerHTML = `
                    <td id="table-buttons">                    
                        <a class="email_list_btn" id="mark_as_read_btn" title="Mark as Read" data-id="${mail[1]["id"]}">
                            <span id="mail_list_seen_ico"><i class="fas fa-eye"></i></span></a>
                        <a class="email_list_btn" id="archive_mail" title="Archive" data-id="${mail[1]["id"]}"><span id="mail_list_arch_ico"><i class="fas fa-archive"></i></span></a>
                    </td>
                    <td id="table-sender">
                        ${mail[1]["sender"]}
                    </td>
                    <td id="table-subject">
                        ${mail[1]["subject"]}
                    </td>
                    <td id="table-timestamp">
                        ${mail[1]["timestamp"]} 
                    </td>
                    `;

                        element.addEventListener("click", () => {
                            show_mail(mail[1]["id"]);
                        });

                        document.querySelector('#emails-view-table').append(element);
                    });

                // Add event listeners to each row

                document.querySelectorAll('#mark_as_read_btn').forEach(
                    elem => {
                        elem.addEventListener("click", () => {
                            fetch('/emails/' + elem.dataset.id, {
                                    method: 'PUT',
                                    body: JSON.stringify({
                                        "read": true
                                    })
                                }
                            );
                            event.stopPropagation();
                        });

                    }
                );

                document.querySelectorAll('#archive_mail').forEach(
                    elem => {
                        elem.addEventListener("click", () => {
                            fetch('/emails/' + elem.dataset.id, {
                                method: 'PUT',
                                body: JSON.stringify({
                                    archived: true
                                })

                            });
                            load_mailbox("inbox");
                            event.stopPropagation();
                        });
                    }
                );
            }
        )
    ;


}


function show_mail(id) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#show-email-view').style.display = 'block';


    fetch('/emails/' + id)
        .then(
            response => response.json()
        ).then(
        email => {
            document.getElementById("sev_heading").innerHTML = `Email View`;

            document.getElementById("sev_subject").innerHTML = `<b>Subject:</b> ${email["subject"]}`;

            document.getElementById("sev_timestamp").innerHTML = `Date: ${email["timestamp"]}`;

            let recipient_srt = "";

            email["recipients"].forEach(
                recipient => recipient_srt += recipient += " "
            );

            let archived_btn = document.getElementById("sev_archive");


            let archived_status = document.getElementById("sev_archive_status");

            document.getElementById("show_inbox_btn").style.display = "none";

            if (!email["archived"]) {
                archived_btn.innerHTML = '<i class="fas fa-box-open"></i>';
                archived_btn.title = "Archive Email";
                archived_status.innerText = 'The mail is not archived';
                archived_btn.dataset.is_archived = "t";
            } else {
                archived_btn.innerHTML = '<i class="fas fa-box"></i>';
                archived_btn.title = "Unarchive Email";
                archived_status.innerText = 'The mail is archived';
                archived_btn.dataset.is_archived = "f";
            }


            if (email["archived"]) {
                document.getElementById("sev_archive").dataset.is_archived = "f";
            } else {
                document.getElementById("sev_archive").dataset.is_archived = "t";
            }


            // First execution of the view:
            if (!archived_btn.classList.contains("has_listener")) {
                archived_btn.addEventListener("click", () => {
                    mail_archive_manipulation(email["id"]);
                });
                archived_btn.className += " has_listener ";
            }

            document.getElementById("sev_recipients").innerHTML = `<b>Recipients:</b> ${recipient_srt}`;

            document.getElementById("sev_body").innerHTML = `${email["body"]}`;

            mark_as_read(email["id"]);

            // Reply Button:
            let reply_btn = document.getElementById("reply-btn");
            reply_btn.addEventListener("click", () => {

                let recipient = email["sender"];
                let subject = email["subject"].startsWith("RE:") ? email["subject"] : "RE: " + email["subject"];
                let body = "On " + email["timestamp"] + " "  + email["sender"] + " wrote:\n\n" + email["body"] + "\n━━━━━━━━━━━\n";


                compose_email({"recipient": recipient,
                                            "subject": subject,
                                            "body": body});
            });
        }
    );

}

function mark_as_read(mail_id) {
    fetch('/emails/' + mail_id, {
        method: 'PUT',
        body: JSON.stringify({
            "read": true
        })
    });
}

function mail_archive_manipulation(mail_id) {


    let archived_btn = document.getElementById("sev_archive");
    let archived_status = document.getElementById("sev_archive_status");

    let is_archived = archived_btn.dataset.is_archived === "t";

    console.log("is_archived " + is_archived);
    fetch('/emails/' + mail_id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: is_archived
        })

    });


    console.log("is_archived:" + is_archived);

    console.log("dataset: " + archived_btn.dataset.is_archived);

    if (archived_btn.dataset.is_archived === "f") {
        archived_btn.innerHTML = '<i class="fas fa-box-open"></i>';
        archived_btn.title = "Archive Email";
        archived_status.innerText = 'The mail is not archived';
        archived_btn.dataset.is_archived = "t";
        console.log("if " + archived_btn.dataset.is_archived);
    } else {
        archived_btn.innerHTML = '<i class="fas fa-box"></i>';
        archived_btn.title = "Unarchive Email";
        archived_status.innerText = 'The mail is archived';
        archived_btn.dataset.is_archived = "f";
        console.log("else " + archived_btn.dataset.is_archived);
    }

    document.getElementById("show_inbox_btn").style.display = "block";


}

function load_inbox() {
    load_mailbox("inbox");
}

