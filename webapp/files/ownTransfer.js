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

    // Get form values
    const transfer_from = document.getElementById('transfer_from')
    const source_account =
      transfer_from.options[
        transfer_from.selectedIndex
      ].attributes.getNamedItem('data-account-id').value
    const transfer_to = document.getElementById('transfer_to')
    const target_account =
      transfer_to.options[transfer_to.selectedIndex].attributes.getNamedItem(
        'data-account-id',
      ).value
    const user_token = await getCookie('user_token')
    const value_element = document.getElementById('value')
    const value = value_element.value
    try {
      // Prepare data to send
      const formData = {
        source_account_id: source_account,
        target_account_id: target_account,
        value: value,
      }
      // Send to Flask backend
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
        alert('Error: ' + (result.message || 'Create account failed'))
      }
    } catch (error) {
      console.error('Error:', error)
    }
  })
