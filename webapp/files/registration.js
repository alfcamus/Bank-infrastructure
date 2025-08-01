document
  .getElementById('registrationForm')
  .addEventListener('submit', async function (e) {
    e.preventDefault()

    // Get form values
    const firstName = document.getElementById('firstName').value
    const lastName = document.getElementById('lastName').value
    const password = document.getElementById('password').value
    const pesel = document.getElementById('pesel').value
    const confirmPassword = document.getElementById('confirmPassword').value

    // Validate password
    if (password !== confirmPassword) {
      alert('Passwords do not match!')
      return
    }

    if (password.length < 8) {
      alert('Password must be at least 8 characters long!')
      return
    }

    try {
      // Hash the password
      const hashedPassword = await sha256(password)

      // Prepare data to send
      const formData = {
        name: firstName,
        surname: lastName,
        pesel: pesel,
        password: hashedPassword,
      }

      // Send to Flask backend
      const response = await fetch('/register', {
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
        alert('Error: ' + (result.message || 'Registration failed'))
      }
    } catch (error) {
      console.error('Error:', error)
    }
  })

async function sha256(message) {
  // Encode the message as UTF-8
  const msgBuffer = new TextEncoder().encode(message)

  // Hash the message
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer)

  // Convert the ArrayBuffer to byte array
  const hashArray = Array.from(new Uint8Array(hashBuffer))

  // Convert bytes to hex string
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')

  return hashHex
}
