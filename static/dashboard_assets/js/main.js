/**
* Template Name: NiceAdmin
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Updated: Apr 20 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */

  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  tinymce.init({
    selector: 'textarea.tinymce-editor',
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons accordion',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: "undo redo | accordion accordionremove | blocks fontfamily fontsize | bold italic underline strikethrough | align numlist bullist | link image | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor codesample | ltr rtl",
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_class_list: [{
        title: 'None',
        value: ''
      },
      {
        title: 'Some class',
        value: 'class-name'
      }
    ],
    importcss_append: true,
    file_picker_callback: (callback, value, meta) => {
      /* Provide file and text for the link dialog */
      if (meta.filetype === 'file') {
        callback('https://www.google.com/logos/google.jpg', {
          text: 'My text'
        });
      }

      /* Provide image and alt text for the image dialog */
      if (meta.filetype === 'image') {
        callback('https://www.google.com/logos/google.jpg', {
          alt: 'My alt text'
        });
      }

      /* Provide alternative source and posted for the media dialog */
      if (meta.filetype === 'media') {
        callback('movie.mp4', {
          source2: 'alt.ogg',
          poster: 'https://www.google.com/logos/google.jpg'
        });
      }
    },
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    skin: useDarkMode ? 'oxide-dark' : 'oxide',
    content_css: useDarkMode ? 'dark' : 'default',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      columns: [{
          select: 2,
          sortSequence: ["desc", "asc"]
        },
        {
          select: 3,
          sortSequence: ["desc"]
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();

// Notice loading
$(document).ready(function() {
  // Load notices
  $.getJSON(URL, function(data) {
      let content = '';
      $.each(data, function(index, notice) {
          let noticeClass = '';
          switch (notice.type) {
              case 'Urgent':
                  noticeClass = 'notice-urgent';
                  break;
              case 'Reminder':
                  noticeClass = 'notice-reminder';
                  break;
              case 'Event':
                  noticeClass = 'notice-event';
                  break;
              default:
                  noticeClass = 'notice-general';
          }
          content += '<div class="notice ' + noticeClass + '">';
          content += '<h3>' + notice.title + '</h3>';
          content += '<p>' + notice.content + '</p>';
          content += '<small>' + notice.date + '</small>';
          content += '</div>';
      });
      $('#notices').html(content);
  });
});

// Package Manager
function handleApprove(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('data-item-id');
  console.log('Approving item:', itemId);  // Add this line
  $.post(`/package_manager/approve/${itemId}`, function(response) {
      if (response.status === 'success') {
          row.style.backgroundColor = 'lightgreen';
          row.querySelectorAll('td').forEach(td => {
            td.style.backgroundColor = 'lightgreen';
          });
          console.log(response.message);
      } else {
          console.error(response.message);
      }
  }).fail(function(jqXHR, textStatus, errorThrown) {
      console.error('Error approving:', textStatus, errorThrown);
  });
}

function handleReject(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('data-item-id');
  console.log('Rejecting item:', itemId);  // Add this line
  $.post(`/package_manager/reject/${itemId}`, function(response) {
      if (response.status === 'success') {
        row.style.backgroundColor = 'lightcoral';
        row.querySelectorAll('td').forEach(td => {
          td.style.backgroundColor = 'lightcoral';
        });
      } else {
          console.error(response.message);
      }
  }).fail(function(jqXHR, textStatus, errorThrown) {
      console.error('Error rejecting:', textStatus, errorThrown);
  });
}

// Webpage loading Dynamic
function loadPage(url) {
  fetch(url)
      .then(response => response.text())
      .then(html => {
          document.getElementById('main').innerHTML = html;
          // loadAdditionalJS();
      })
      .catch(error => console.error('Error loading page:', error));
}
// function loadAdditionalJS() {
//   // Example of loading additional JS after content is loaded
//   const script = document.createElement('script');
//   script.src = '/static/dashboard_assets/js/main.js';  // Path to your specific JS file
//   document.body.appendChild(script);
// }

// Society Delete Button
$(document).ready(function() {
  $(document).on('click', '.sodelete-btn', function() {
      if (confirm("Are you sure you want to delete this Society?")) {
          var SocietyId = $(this).data('id');
          var row = $(this).closest('tr');

          $.ajax({
              url: '/admin/delete/' + SocietyId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete Society.');
                  }
              },
              error: function() {
                alert('Society is Linked with member so it cannot be deleted');;
              }
          });
      }
  });
});
// function handleDelete(button) {
//   if(confirm("Are you sure you want to delete this Society?")){
//     const row = button.closest('tr');
//     const itemId = row.getAttribute('row-id');
//     console.log('Deleting item:', itemId);

//     $.post(`/admin/delete/${itemId}`, function(response) {
//       if (response.status === 'success') {
//         row.style.backgroundColor = 'lightcoral';
//         row.querySelectorAll('td').forEach(td => {
//           td.style.backgroundColor = 'lightcoral';
//         });
//       } else {
//         alert(response.message); // Display error message in alert
//         console.error(response.message);
//       }
//     }).fail(function(jqXHR, textStatus, errorThrown) {
//       console.error('Error deleting:', textStatus, errorThrown);
//       alert('Society is Linked with member so it cannot be deleted'); // Display generic error message
//     });
//   }
// }



// Member Approve Button (Secretary)
function handleApproveMember(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Approving item:', itemId);

  $.post(`/secretary/approve/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightgreen';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightgreen';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error approving:', textStatus, errorThrown);
  });
}

function handleRejectMember(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Approving item:', itemId);

  $.post(`/secretary/reject/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightcoral';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightcoral';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error rejecting:', textStatus, errorThrown);
  });
}

// function handleDeleteMember(button) {
//   const row = button.closest('tr');
//   const itemId = row.getAttribute('row-id');
//   console.log('Deleting item:', itemId);

//   $.post(`/secretary/delete/${itemId}`, function(response) {
//     if (response.status === 'success') {
//       row.style.backgroundColor = 'lightcoral';
//       row.querySelectorAll('th, td').forEach(cell => {
//         cell.style.backgroundColor = 'lightcoral';
//       });
//     } else {
//       alert(response.message); 
//       console.error(response.message);
//     }
//   }).fail(function(jqXHR, textStatus, errorThrown) {
//     console.error('Error deleting:', textStatus, errorThrown);
//     alert(errorThrown)
//   });
// }

// Member Delete button (Secretary)
$(document).ready(function() {
  $(document).on('click', '.mdelete-btn', function() {
      if (confirm("Are you sure you want to delete this Member?")) {
          var memberId = $(this).data('id');
          var row = $(this).closest('tr');

          $.ajax({
              url: '/secretary/delete/' + memberId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete the member.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete the member.');
              }
          });
      }
  });
});

// Notice editor
$(document).ready(function() {  
  // Handling blur event for editable cells
  jQuery(document).on('blur', 'td[contenteditable="true"]', function() {
      var cell = $(this);
      var column = cell.data('column');
      var value;
      
      // Check if it's a dropdown select
      if (cell.find('select').length > 0) {
          value = cell.find('select').val();
      } else {
          value = cell.text();
      }
      
      var id = cell.data('id');
      
      console.log(value);
      
      // AJAX request
      $.ajax({
          url: '/secretary/update_notice',
          method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({ n_id: id, column: column, value: value }),
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.error('Error:', error);
          }
      });
  });
});

// Notice Deleting
$(document).ready(function() {
  $(document).on('click', '.delete-btn', function() {
      if (confirm("Are you sure you want to delete this Notice?")) {
          var noticeId = $(this).data('id');
          var row = $(this).closest('tr');

          $.ajax({
              url: '/secretary/delete_notice/' + noticeId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete the notice.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete the notice.');
              }
          });
      }
  });
});


// Security Approve Button (Secretary)
function handleApproveSecurity(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Approving security:', itemId);

  $.post(`/secretary/approve_security/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightgreen';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightgreen';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error approving:', textStatus, errorThrown);
  });
}
//  Security Reject Button (Secretary)
function handleRejectSecurity(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Rejecting Security:', itemId);

  $.post(`/secretary/reject_security/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightcoral';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightcoral';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error rejecting:', textStatus, errorThrown);
  });
}


//  Security Delete Button (Secretary)
$(document).ready(function() {
  $(document).on('click', '.sdelete-btn', function() {
      if (confirm("Are you sure you want to delete this particular Security Personnel?")) {
          var securityId = $(this).data('id');
          var row = $(this).closest('tr');
          $.ajax({
              url: '/secretary/delete_security/' + securityId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete this Personnel.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete this Security Personnel.');
              }
          });
      }
  });
});

//Secretary Delete Button (Admin) 
$(document).ready(function() {
  $(document).on('click', '.secdelete-btn', function() {
      if (confirm("Are you sure you want to delete this particular Secretary?")) {
          var secretaryId = $(this).data('id');
          var row = $(this).closest('tr');
          $.ajax({
              url: '/admin/delete_security/' + secretaryId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete this Secretary.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete this Secretary.');
              }
          });
      }
  });
});
// Secretary Approve Button (Admin)
function handleApproveSecretary(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Approving secretary:', itemId);

  $.post(`/admin/approve_secretary/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightgreen';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightgreen';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error approving:', textStatus, errorThrown);
  });
}


function handleRejectSecretary(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Rejecting Secretary:', itemId);

  $.post(`/admin/reject_secretary/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightcoral';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightcoral';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error rejecting:', textStatus, errorThrown);
  });
}

$(document).ready(function() {
  $(document).on('submit','#profileForm', function(event) {
      event.preventDefault();

      var phoneNo = $('#phone_no').val();
      var email = $('#email').val();
      var phonePattern = /^\d{10}$/;
      var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      // Perform client-side validation
      if (!phonePattern.test(phoneNo)) {
          alert('Phone number must be exactly 10 digits long.');
          return; // Prevent form submission
      }

      if (!emailPattern.test(email)) {
          alert('Please enter a valid email address.');
          return; // Prevent form submission
      }

      // Proceed with AJAX form submission if all validations pass
      var formData = {
          uid: $('#uid').val(),
      };

      $.ajax({
          type: 'POST',
          url: '/profile/check_value',
          contentType: 'application/json',
          data: JSON.stringify({ values: formData }),
          success: function(response) {
              console.log(response);
              $('#status-uid').text(response.uidExists[0] ? 'Username already exists' : '');

              if (!response.uidExists[0]) {
                  // Now submit the form using plain JavaScript
                  document.getElementById('profileForm').submit();
              }
          }
      });
  });

});

function handleApproveMember(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Approving secretary:', itemId);

  $.post(`/secretary/approve/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightgreen';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightgreen';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error approving:', textStatus, errorThrown);
  });
}

function handleRejectMember(button) {
  const row = button.closest('tr');
  const itemId = row.getAttribute('row-id');
  console.log('Rejecting Secretary:', itemId);

  $.post(`/secretary/reject/${itemId}`, function(response) {
    if (response.status === 'success') {
      row.style.backgroundColor = 'lightcoral';
      row.querySelectorAll('td').forEach(td => {
        td.style.backgroundColor = 'lightcoral';
      });
    } else {
      alert(response.message);
      console.error(response.message);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error rejecting:', textStatus, errorThrown);
  });
}

// Password checking
$(document).ready(function() {
  $(document).on('submit','#passwordForm', function(event) {
      event.preventDefault();

      var newpassword = $('#newPassword').val();
      var renewpassword = $('#renewPassword').val();


      // Perform client-side validation
      if (newpassword!=renewpassword) {
          alert("New passwords do not match");
          return; // Prevent form submission
      }

      // Proceed with AJAX form submission if all validations pass
      var formData = {
          password: $('#currentPassword').val(),
      };

      $.ajax({
          type: 'POST',
          url: '/profile/check_password',
          contentType: 'application/json',
          data: JSON.stringify({ values: formData }),
          success: function(response) {
              console.log(response);
              $('#status-password').text(response.passwordEqual[0] ? '' : 'Current Password is incorrect');

              if (response.passwordEqual[0]) {
                  // Now submit the form using plain JavaScript
                  document.getElementById('passwordForm').submit();
              }
          }
      });
  });

});


//Permission Delete Button (Security) 
$(document).ready(function() {
  $(document).on('click', '.pdelete-btn', function() {
      if (confirm("Are you sure you want to delete this particular permission?")) {
          var itemId = $(this).data('id');
          var row = $(this).closest('tr');
          $.ajax({
              url: '/package_manager/delete_permission/' + itemId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete this permission.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete this Permission.');
              }
          });
      }
  });
});


//Permission Delete Button (Member)
$(document).ready(function() {
  $(document).on('click', '.pmdelete-btn', function() {
      if (confirm("Are you sure you want to delete this particular permission?")) {
          var itemId = $(this).data('id');
          var row = $(this).closest('tr');
          $.ajax({
              url: '/package_manager/member_delete_permission/' + itemId,
              type: 'POST',
              success: function(response) {
                  if (response.success) {
                      row.remove();
                  } else {
                      alert('Failed to delete this permission.');
                  }
              },
              error: function() {
                  alert('Error occurred while trying to delete this Permission.');
              }
          });
      }
  });
});
