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
  .getElementById('account_form')
  .addEventListener('submit', async function (e) {
    e.preventDefault()

    // Get form values
    const account_type = document.getElementById('account_type').value
    const user_token = await getCookie('user_token')
    try {
      // Prepare data to send
      const formData = {
        account_type: account_type,
        login: JSON.parse(atob(user_token)).data.client.login,
      }
      // Send to Flask backend
      const response = await fetch('/create-new-account', {
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
