const petOwnerCardData = [
    {
        id: 'dynamicCardContainer',
        tabs: [
            {
                title: 'Request Services',
                content: `
                    <h2 class="mb-3 text-2xl font-bold text-gray-900">
                        Comprehensive Veterinary Services
                    </h2>
                    <p class="mb-3 text-gray-600">
                        Our clinic offers a wide array of services tailored to your pet's needs. From advanced diagnostics and imaging services such as X-rays and echography, to wellness exams, parasite tests, and grooming services, we are equipped to provide top-notch care.
                    </p>
                    <a href="/dashboard/services/request-service/" class="inline-flex items-center font-medium text-blue-600 hover:text-blue-800">
                        Request Services
                        <svg class="ml-2 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7m8-7H3" />
                        </svg>
                    </a>
                `
            },
            {
                title: 'Payments',
                content: `
                    <h2 class="mb-3 text-2xl font-bold text-gray-900">
                        Easy Online Payments
                    </h2>
                    <p class="mb-3 text-gray-600">
                        Simplify the payment process with our secure online payment system. Whether it's for routine check-ups, diagnostic services, or grooming, you can manage all your payments conveniently from anywhere.
                    </p>
                    <a href="/dashboard/services/make-payment/" class="inline-flex items-center font-medium text-blue-600 hover:text-blue-800">
                        Make a Payment
                        <svg class="ml-2 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7m8-7H3" />
                        </svg>
                    </a>
                `
            },
            {
                title: 'Appointments',
                content: `
                    <h2 class="mb-3 text-2xl font-bold text-gray-900">
                        Upcoming Appointments
                    </h2>
                    <p class="mb-3 text-gray-600">
                        Keep track of all scheduled appointments for your pets. Our system makes it easy to view upcoming visits, including dates, times, and the nature of each appointment.
                    </p>
                    <a href="/dashboard/appointments/appointments-list/" class="inline-flex items-center font-medium text-blue-600 hover:text-blue-800">
                        View Appointments
                        <svg class="ml-2 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    </a>
                `
            },
            {
                title: 'Requested Services',
                content: `
                    <h2 class="mb-3 text-2xl font-bold text-gray-900">
                        Service Requests
                    </h2>
                    <p class="mb-3 text-gray-600">
                        View a comprehensive list of all the services you've requested for your pet, including status updates on pending, approved, and completed services.
                    </p>
                    <a href="/dashboard/services/request-service-list/" class="inline-flex items-center font-medium text-blue-600 hover:text-blue-800">
                        Manage Requests
                        <svg class="ml-2 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </a>
                `
            }
        ]
    },
];

`
                        <h2 class="mb-3 text-2xl font-bold text-gray-900">
                            Pet Owner Directory
                        </h2>
                        <p class="mb-3 text-gray-600">
                            Browse the directory of pet owners to facilitate communication and manage appointments effectively. Our platform provides detailed profiles of pet owners, including contact information, pet details, and appointment histories.
                        </p>
                        <a href="/pets/petowner/list/" class="inline-flex items-center font-medium text-blue-600 hover:text-blue-800">
                            Explore Pet Owner Profiles
                            <svg class="ml-2 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7m8-7H3" />
                            </svg>
                        </a>
                    `

                    <svg width="30px" height="30px" viewBox="0 0 1024 1024" class="icon" version="1.1"
                    stroke-width="8.192">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                        <path
                            d="M212 32h600c32.8 0 60 27.2 60 60v840c0 32.8-27.2 60-60 60h-600c-32.8 0-60-27.2-60-60v-840C152 59.2 179.2 32 212 32z"
                            fill="#FFFFFF"></path>
                        <path
                            d="M414.4 876H271.2c-10.4 0-19.2-8.8-19.2-19.2V713.6c0-10.4 8.8-19.2 19.2-19.2h143.2c10.4 0 19.2 8.8 19.2 19.2v143.2c0 10.4-8.8 19.2-19.2 19.2z"
                            fill="#FFFFFF"></path>
                        <path
                            d="M812 1000h-600c-37.6 0-68-30.4-68-68v-840C144 54.4 174.4 24 212 24h600c37.6 0 68 30.4 68 68v840c0 37.6-30.4 68-68 68zM212 40C183.2 40 160 63.2 160 92v840c0 28.8 23.2 52 52 52h600c28.8 0 52-23.2 52-52v-840c0-28.8-23.2-52-52-52h-600z"
                            fill="#ed719e"></path>
                        <path
                            d="M414.4 330.4H271.2c-10.4 0-19.2-8.8-19.2-19.2v-144c0-10.4 8.8-19.2 19.2-19.2h143.2c10.4 0 19.2 8.8 19.2 19.2v143.2c0 11.2-8.8 20-19.2 20z"
                            fill="#ff8c82"></path>
                        <path
                            d="M414.4 338.4H271.2c-15.2 0-27.2-12-27.2-27.2v-144c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v143.2c0 15.2-12 28-27.2 28zM271.2 156c-6.4 0-11.2 4.8-11.2 11.2v143.2c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V167.2c0-6.4-4.8-11.2-11.2-11.2H271.2z"
                            fill="#ed719e"></path>
                        <path
                            d="M414.4 603.2H271.2c-10.4 0-19.2-8.8-19.2-19.2V440c0-10.4 8.8-19.2 19.2-19.2h143.2c10.4 0 19.2 8.8 19.2 19.2v144c0 10.4-8.8 19.2-19.2 19.2z"
                            fill="#ff8c82"></path>
                        <path
                            d="M414.4 611.2H271.2c-15.2 0-27.2-12-27.2-27.2V440c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v144c0 14.4-12 27.2-27.2 27.2zM271.2 428.8c-6.4 0-11.2 4.8-11.2 11.2v144c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V440c0-6.4-4.8-11.2-11.2-11.2H271.2zM414.4 884H271.2c-15.2 0-27.2-12-27.2-27.2V713.6c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v143.2c0 15.2-12 27.2-27.2 27.2zM271.2 701.6c-6.4 0-11.2 4.8-11.2 11.2V856c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V713.6c0-6.4-4.8-11.2-11.2-11.2H271.2zM414.4 338.4H271.2c-15.2 0-27.2-12-27.2-27.2v-144c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v143.2c0 15.2-12 28-27.2 28zM271.2 156c-6.4 0-11.2 4.8-11.2 11.2v143.2c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V167.2c0-6.4-4.8-11.2-11.2-11.2H271.2z"
                            fill="#ed719e"></path>
                        <path
                            d="M414.4 611.2H271.2c-15.2 0-27.2-12-27.2-27.2V440c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v144c0 14.4-12 27.2-27.2 27.2zM271.2 428.8c-6.4 0-11.2 4.8-11.2 11.2v144c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V440c0-6.4-4.8-11.2-11.2-11.2H271.2zM414.4 884H271.2c-15.2 0-27.2-12-27.2-27.2V713.6c0-15.2 12-27.2 27.2-27.2h143.2c15.2 0 27.2 12 27.2 27.2v143.2c0 15.2-12 27.2-27.2 27.2zM271.2 701.6c-6.4 0-11.2 4.8-11.2 11.2V856c0 6.4 4.8 11.2 11.2 11.2h143.2c6.4 0 11.2-4.8 11.2-11.2V713.6c0-6.4-4.8-11.2-11.2-11.2H271.2zM768 247.2H548c-4.8 0-8-3.2-8-8s3.2-8 8-8H768c4.8 0 8 3.2 8 8s-3.2 8-8 8z"
                            fill="#ed719e"></path>
                        <path d="M768 520H548c-4.8 0-8-3.2-8-8s3.2-8 8-8H768c4.8 0 8 3.2 8 8s-3.2 8-8 8z"
                            fill="#ed719e"></path>
                        <path
                            d="M766.4 792.8H546.4c-4.8 0-8-3.2-8-8s3.2-8 8-8h220c4.8 0 8 3.2 8 8s-4 8-8 8z"
                        ></path>
                    </g>
                </svg>
                <button
                    class="h-fit p-[2px] flex justify-center text-sm font-medium text-gray-900 rounded-lg bg-gradient-to-br from-pink-500 to-orange-400 hover:text-white focus:ring-4 focus:outline-none focus:ring-pink-200">
                    <span
                        class="w-60 px-5 py-2.5 bg-white rounded-md hover:bg-opacity-0 transition-all ease-in duration-75">
                        <a href="/dashboard/services/request-service-list/">
                            Manage Requests
                        </a>
                    </span>
                </button>
            </div>