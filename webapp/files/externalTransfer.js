function renderAlert(message) {
  // Create the alert element
  const alertDiv = document.createElement('div')
  alertDiv.className = 'alert alert-warning alert-dismissible fade show'
  alertDiv.setAttribute('role', 'alert')

  // Add the alert content
  alertDiv.innerHTML = `
<strong>Warning!</strong> ${message}
<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
`

  // Add the alert to the page (at the top of the body)
  document.body.insertBefore(alertDiv, document.body.firstChild)

  // Initialize Bootstrap's alert functionality
  // This is the key part that makes the close button work
  document
    .querySelector('.alert .btn-close')
    .addEventListener('click', function () {
      const alert = bootstrap.Alert.getOrCreateInstance(alertDiv)
      alert.close()
    })
}

let target_account_id;

document
  .getElementById('login_search_button')
  .addEventListener('click', async function (e) {
    // In a real implementation, this would filter the transfer_to options
    // or make an API call to search for accounts
    try {
      document.getElementById('search_spinner').style.display = 'inline-block'
      const login = document.getElementById('transfer_to_search').value
      const formData = {
        login: login,
      }
      const response = await fetch('/get-checking-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      let body = await response.json()
      if (body.status === 'error') {
        renderAlert(body.message)
        document.getElementById('search_spinner').style.display = 'none'
        document.getElementById('checkmark_tick').style.display = 'none'
        document.getElementById('fail_symbol').style.display = 'inline-block'
      } else {
        target_account_id = body.id
        document.getElementById('search_spinner').style.display = 'none'
        document.getElementById('checkmark_tick').style.display = 'inline-block'
      }
    } catch (error) {
      console.error('Error:', error)
    }
  })

async function getCookie(name) {
  try {
    const cookie = await cookieStore.get(name)
    return cookie ? cookie.value : null
  } catch (error) {
    console.error('Cookie Store API not supported:', error)
    return getCookies()[name] // Fallback
  }
}

document
  .getElementById('transfer_form')
  .addEventListener('submit', async function (e) {
    e.preventDefault()
    // Get the button
    const button = document.getElementById('TransferButton')

    // Disable it (Bootstrap style + prevents clicks)
    button.classList.add('disabled')
    button.setAttribute('disabled', '')
    // Get form values
    const transfer_from = document.getElementById('transfer_from')
    const source_account =
      transfer_from.options[
        transfer_from.selectedIndex
      ].attributes.getNamedItem('data-account-id').value
    const value_element = document.getElementById('value')
    const value = value_element.value
    try {
      // Prepare data to send
      const formData = {
        source_account_id: source_account,
        target_account_id: target_account_id,
        value: value,
      }
      // Send to Flask backend
      console.log(target_account_id)
      if (!target_account_id) {
        renderAlert('Please, input correct login of the desirable user.')
      }
      const response = await fetch('/make-transaction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const result = await response.json()

      if (response.ok && result.redirect_url) {
        window.location.href = result.redirect_url // Perform redirect
      } else {
        renderAlert(result.message)
      }
    } catch (error) {
      console.error('Error:', error)
    }
  })
