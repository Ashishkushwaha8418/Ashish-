<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <title>
   Age Calculator App
  </title>
  <script src="https://cdn.tailwindcss.com">
  </script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap" rel="stylesheet"/>
  <style>
   body {
      font-family: 'Inter', sans-serif;
    }
  </style>
 </head>
 <body class="bg-gradient-to-br from-blue-100 to-indigo-200 min-h-screen flex items-center justify-center p-4">
  <div class="bg-white rounded-3xl shadow-xl max-w-md w-full p-8">
   <div class="flex flex-col items-center mb-8">
    <img alt="Illustration of a calendar and clock symbolizing age calculation" class="w-24 h-24 mb-4" height="100" src="https://storage.googleapis.com/a1aa/image/56119117-3b42-436b-c640-4c8bd85ea841.jpg" width="100"/>
    <h1 class="text-3xl font-semibold text-indigo-700">
     Age Calculator
    </h1>
    <p class="text-gray-600 mt-2 text-center">
     Enter your birth date to find out your exact age.
    </p>
   </div>
   <form class="space-y-6" id="ageForm">
    <div>
     <label class="block text-gray-700 font-medium mb-2" for="birthDate">
      Birth Date
     </label>
     <input class="w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition" id="birthDate" max="" name="birthDate" required="" type="date"/>
    </div>
    <button class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-lg shadow-md transition" type="submit">
     Calculate Age
    </button>
   </form>
   <div class="mt-8 bg-indigo-50 border border-indigo-200 rounded-lg p-6 text-center text-indigo-900 text-lg font-semibold hidden" id="result">
    <!-- Age result will appear here -->
   </div>
  </div>
  <script>
   const birthDateInput = document.getElementById('birthDate');
    const ageForm = document.getElementById('ageForm');
    const resultDiv = document.getElementById('result');

    // Set max date to today
    const today = new Date().toISOString().split('T')[0];
    birthDateInput.setAttribute('max', today);

    ageForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const birthDateValue = birthDateInput.value;
      if (!birthDateValue) {
        resultDiv.textContent = 'Please select your birth date.';
        resultDiv.classList.remove('hidden');
        return;
      }

      const birthDate = new Date(birthDateValue);
      const now = new Date();

      if (birthDate > now) {
        resultDiv.textContent = 'Birth date cannot be in the future.';
        resultDiv.classList.remove('hidden');
        return;
      }

      // Calculate age components
      let years = now.getFullYear() - birthDate.getFullYear();
      let months = now.getMonth() - birthDate.getMonth();
      let days = now.getDate() - birthDate.getDate();

      if (days < 0) {
        months -= 1;
        // Get days in previous month
        const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
        days += prevMonth.getDate();
      }

      if (months < 0) {
        years -= 1;
        months += 12;
      }

      // Format result string
      let ageString = '';
      if (years > 0) ageString += `${years} year${years > 1 ? 's' : ''} `;
      if (months > 0) ageString += `${months} month${months > 1 ? 's' : ''} `;
      if (days > 0) ageString += `${days} day${days > 1 ? 's' : ''}`;

      if (ageString === '') ageString = '0 days';

      resultDiv.textContent = `You are ${ageString.trim()} old.`;
      resultDiv.classList.remove('hidden');
    });
  </script>
 </body>
</html>
