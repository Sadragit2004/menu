    // مقداردهی اولیه Select2
        $(document).ready(function() {
            // فارسی‌سازی Select2
            $.fn.select2.defaults.set("language", "fa");

            // فعال کردن Select2 برای انتخاب دسته‌بندی در مودال غذا
            $('.select2-category').select2({
                placeholder: "انتخاب دسته‌بندی",
                allowClear: true,
                width: '100%',
                dir: 'rtl'
            });

            // فعال کردن Select2 برای انتخاب دسته‌بندی در مودال افزودن دسته‌بندی
            $('.select2-category-all').select2({
                placeholder: "جستجو و انتخاب دسته‌بندی",
                allowClear: true,
                width: '100%',
                dir: 'rtl'
            });

            // بستن Select2 هنگام بستن مودال
            $('.close-modal').on('click', function() {
                $('.select2-category').select2('close');
                $('.select2-category-all').select2('close');
            });
        });

function openModal(modalId) {
    console.log('باز کردن مودال:', modalId);
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        modal.style.display = 'flex';
        console.log('مودال باز شد');
    } else {
        console.error('مودال پیدا نشد:', modalId);
    }
}

        // مدیریت مودال‌ها
        document.addEventListener('DOMContentLoaded', function() {
            // مدیریت تب‌ها
            const tabButtons = document.querySelectorAll('.tab-btn');
            const tabContents = document.querySelectorAll('.tab-content');

            tabButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const tabId = this.getAttribute('data-tab');

                    // Update active tab button
                    tabButtons.forEach(btn => {
                        btn.classList.remove('active');
                        btn.classList.remove('text-blue-600', 'border-blue-600');
                        btn.classList.add('text-gray-500', 'border-transparent');
                    });
                    this.classList.add('active');
                    this.classList.remove('text-gray-500', 'border-transparent');
                    this.classList.add('text-blue-600', 'border-blue-600');

                    // Show active tab content
                    tabContents.forEach(content => {
                        content.classList.remove('active');
                    });
                    document.getElementById(`${tabId}-tab`).classList.add('active');
                });
            });

            // دکمه‌های دسکتاپ
            document.getElementById('add-food-btn')?.addEventListener('click', () => openFoodModal());
            document.getElementById('add-first-food-btn')?.addEventListener('click', () => openFoodModal());
            document.getElementById('manage-categories-btn')?.addEventListener('click', () => document.getElementById('category-modal').style.display = 'flex');
            document.getElementById('restaurant-settings-btn')?.addEventListener('click', () => document.getElementById('restaurant-modal').style.display = 'flex');
            document.getElementById('add-new-category-btn')?.addEventListener('click', () => openAddCategoryModal());
            document.getElementById('add-category-mobile-btn')?.addEventListener('click', () => openQuickCategoryModal());
            document.getElementById('quick-category-btn')?.addEventListener('click', () => openQuickCategoryModal());

            // Floating Action Button
            document.getElementById('fab-main')?.addEventListener('click', function() {
                this.classList.toggle('active');
                document.getElementById('fab-menu').classList.toggle('active');
            });

            document.getElementById('fab-add-food')?.addEventListener('click', () => {
                openFoodModal();
                document.getElementById('fab-menu').classList.remove('active');
                document.getElementById('fab-main').classList.remove('active');
            });

            document.getElementById('fab-add-category')?.addEventListener('click', () => {
                openAddCategoryModal();
                document.getElementById('fab-menu').classList.remove('active');
                document.getElementById('fab-main').classList.remove('active');
            });

            document.getElementById('fab-quick-category')?.addEventListener('click', () => {
                openQuickCategoryModal();
                document.getElementById('fab-menu').classList.remove('active');
                document.getElementById('fab-main').classList.remove('active');
            });

            document.getElementById('fab-restaurant-settings')?.addEventListener('click', () => {
                document.getElementById('restaurant-modal').style.display = 'flex';
                document.getElementById('fab-menu').classList.remove('active');
                document.getElementById('fab-main').classList.remove('active');
            });

            // بستن همه مودال‌ها
            document.querySelectorAll('.close-modal').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.modal').forEach(modal => {
                        modal.style.display = 'none';
                    });
                });
            });

            // پیش‌نمایش تصاویر
            document.getElementById('food-image')?.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.getElementById('food-image-preview');
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });

            document.getElementById('category-icon')?.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.getElementById('category-icon-preview');
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });

            document.getElementById('restaurant-logo')?.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.getElementById('restaurant-logo-preview');
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });

            // مدیریت دسته‌بندی‌ها
            document.querySelectorAll('.category-sidebar-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const categoryId = this.getAttribute('data-category');
                    const menuCategoryId = this.getAttribute('data-menu-category-id');
                    currentSelectedCategory = categoryId;
                    currentSelectedMenuCategoryId = menuCategoryId;

                    document.querySelectorAll('.category-sidebar-btn').forEach(b => b.classList.remove('category-active'));
                    this.classList.add('category-active');

                    document.querySelectorAll('.foods-section').forEach(section => section.classList.remove('active'));

                    if (categoryId === 'all') {
                        document.getElementById('foods-all').classList.add('active');
                        document.getElementById('current-category-text').textContent = 'همه غذاها';
                    } else {
                        document.getElementById(`foods-category-${categoryId}`).classList.add('active');
                        const categoryName = this.querySelector('.category-name').textContent;
                        document.getElementById('current-category-text').textContent = `غذاهای ${categoryName}`;
                    }

                    filterFoods();
                });
            });

            // کلیک روی افزودن غذا در دسته‌بندی‌ها
            document.addEventListener('click', (e) => {
                if (e.target.closest('.add-food-to-category')) {
                    const menuCategoryId = e.target.closest('.add-food-to-category').getAttribute('data-category');
                    openFoodModal(menuCategoryId);
                }
            });

            // Search and Filter
            document.getElementById('search-input')?.addEventListener('input', function() {
                const clearBtn = document.getElementById('clear-search');
                if (this.value) {
                    clearBtn.classList.remove('hidden');
                } else {
                    clearBtn.classList.add('hidden');
                }
                filterFoods();
            });

            document.getElementById('clear-search')?.addEventListener('click', function() {
                document.getElementById('search-input').value = '';
                this.classList.add('hidden');
                filterFoods();
            });

            document.getElementById('status-filter')?.addEventListener('change', function() {
                filterFoods();
            });

            // مدیریت عملیات غذاها
            document.addEventListener('click', async (e) => {
                // افزودن غذا به منو
                if (e.target.closest('.add-food-btn')) {
                    const foodId = e.target.closest('.add-food-btn').getAttribute('data-food-id');
                    await addFoodToMenu(foodId);
                }

                // حذف غذا از منو
                if (e.target.closest('.remove-food-btn')) {
                    const foodId = e.target.closest('.remove-food-btn').getAttribute('data-food-id');
                    await removeFoodFromMenu(foodId);
                }

                if (e.target.closest('.edit-food-btn')) {
                    const foodId = e.target.closest('.edit-food-btn').getAttribute('data-food-id');
                    await loadFoodData(foodId);
                }

                if (e.target.closest('.toggle-food-status')) {
                    const foodId = e.target.closest('.toggle-food-status').getAttribute('data-food-id');
                    await toggleFoodStatus(foodId);
                }

                if (e.target.closest('.delete-food-btn')) {
                    const foodId = e.target.closest('.delete-food-btn').getAttribute('data-food-id');
                    if (confirm('آیا از حذف این غذا مطمئن هستید؟')) {
                        await deleteFood(foodId);
                    }
                }

                if (e.target.closest('.toggle-category-status')) {
                    const categoryId = e.target.closest('.toggle-category-status').getAttribute('data-category-id');
                    await toggleMenuCategoryStatus(categoryId);
                }

                if (e.target.closest('.delete-category-sidebar')) {
                    const categoryId = e.target.closest('.delete-category-sidebar').getAttribute('data-category-id');
                    if (confirm('آیا از حذف این دسته‌بندی از منو مطمئن هستید؟')) {
                        await deleteMenuCategory(categoryId);
                    }
                }
            });

            // ارسال فرم‌ها
            document.getElementById('food-form')?.addEventListener('submit', async function(e) {
                e.preventDefault();
                await submitFoodForm(this);
            });

            document.getElementById('add-category-form')?.addEventListener('submit', async function(e) {
                e.preventDefault();
                await submitCategoryForm(this);
            });

            document.getElementById('restaurant-form')?.addEventListener('submit', async function(e) {
                e.preventDefault();
                await submitRestaurantForm(this);
            });

            // مدیریت انتخاب سریع دسته‌بندی‌ها
            const confirmBtn = document.getElementById('confirm-categories-btn');
            if (confirmBtn) {
                confirmBtn.addEventListener('click', confirmAndAddCategories);
            }

            const selectAllBtn = document.getElementById('select-all-categories');
            const deselectAllBtn = document.getElementById('deselect-all-categories');

            if (selectAllBtn) {
                selectAllBtn.addEventListener('click', selectAllCategories);
            }
            if (deselectAllBtn) {
                deselectAllBtn.addEventListener('click', deselectAllCategories);
            }

            // بارگذاری اولیه
            document.querySelector('[data-category="all"]')?.click();
        });

        // متغیرهای سراسری
        let currentSelectedCategory = 'all';
        let currentSelectedMenuCategoryId = null;
        let selectedCategories = new Map();

        // توابع جدید برای مدیریت انتخاب غذاها
        async function addFoodToMenu(foodId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/foods/${foodId}/toggle-selection/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                });

                const result = await response.json();

                if (result.success) {
                    // Update UI
                    const foodCard = document.querySelector(`.food-card[data-food-id="${foodId}"]`);
                    foodCard.classList.remove('available');
                    foodCard.classList.add('selected');

                    const button = foodCard.querySelector('.add-food-btn');
                    button.classList.remove('add-food-btn', 'text-green-500');
                    button.classList.add('remove-food-btn', 'text-red-500');
                    button.innerHTML = '<i class="fas fa-times"></i>';
                    button.setAttribute('title', 'حذف از منو');

                    const badge = foodCard.querySelector('.absolute.bottom-3.left-3 span');
                    badge.classList.remove('bg-red-500');
                    badge.classList.add('bg-green-500');
                    badge.innerHTML = '<i class="fas fa-check ml-1"></i> انتخاب شده';

                    // Show success message
                    showNotification('غذا با موفقیت به منو اضافه شد', 'success');
                } else {
                    showNotification('خطا در افزودن غذا به منو', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('خطا در ارتباط با سرور', 'error');
            }
        }

        async function removeFoodFromMenu(foodId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/foods/${foodId}/toggle-selection/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                });

                const result = await response.json();

                if (result.success) {
                    // If we're in the selected foods tab, remove the card
                    if (document.getElementById('selected-foods-tab').classList.contains('active')) {
                        const foodCard = document.querySelector(`.food-card[data-food-id="${foodId}"]`);
                        foodCard.remove();
                    } else {
                        // If we're in the all foods tab, update the card
                        const foodCard = document.querySelector(`.food-card[data-food-id="${foodId}"]`);
                        foodCard.classList.remove('selected');
                        foodCard.classList.add('available');

                        const button = foodCard.querySelector('.remove-food-btn');
                        button.classList.remove('remove-food-btn', 'text-red-500');
                        button.classList.add('add-food-btn', 'text-green-500');
                        button.innerHTML = '<i class="fas fa-plus"></i>';
                        button.setAttribute('title', 'افزودن به منو');

                        const badge = foodCard.querySelector('.absolute.bottom-3.left-3 span');
                        badge.classList.remove('bg-green-500');
                        badge.classList.add('bg-red-500');
                        badge.innerHTML = '<i class="fas fa-plus ml-1"></i> قابل انتخاب';
                    }

                    // Show success message
                    showNotification('غذا با موفقیت از منو حذف شد', 'success');
                } else {
                    showNotification('خطا در حذف غذا از منو', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('خطا در ارتباط با سرور', 'error');
            }
        }

        // باز کردن مودال غذا با دسته‌بندی انتخاب شده
        function openFoodModal(selectedMenuCategory = '') {
            document.getElementById('modal-title').textContent = 'افزودن غذا';
            document.getElementById('food-form').reset();
            document.getElementById('food-id').value = '';
            document.getElementById('food-image-preview').style.display = 'none';

            // ریست کردن Select2
            $('.select2-category').val('').trigger('change');

            // اگر دسته‌بندی خاصی انتخاب شده و "همه" نیست، آن را در select پیش‌فرض قرار بده
            if (selectedMenuCategory && selectedMenuCategory !== 'all') {
                $('.select2-category').val(selectedMenuCategory).trigger('change');
            } else if (currentSelectedMenuCategoryId && currentSelectedCategory !== 'all') {
                $('.select2-category').val(currentSelectedMenuCategoryId).trigger('change');
            }

            document.getElementById('food-modal').style.display = 'flex';
        }

        // باز کردن مودال افزودن دسته‌بندی
        function openAddCategoryModal() {
            document.getElementById('add-category-form').reset();
            document.getElementById('category-icon-preview').style.display = 'none';

            // ریست کردن Select2
            $('.select2-category-all').val('').trigger('change');
            document.getElementById('add-category-modal').style.display = 'flex';
        }

        // باز کردن مودال انتخاب سریع
        function openQuickCategoryModal() {
            selectedCategories.clear();
            document.getElementById('quick-category-modal').style.display = 'flex';
            updateSelectedCategoriesUI();
            document.getElementById('category-search').value = '';
            loadCategoryTree();
        }

        // فیلتر غذاها
        function filterFoods() {
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            const statusFilter = document.getElementById('status-filter').value;

            const activeTab = document.querySelector('.tab-content.active').id;

            if (activeTab === 'selected-foods-tab') {
                 

                filterFoodsInSelectedTab(searchTerm, statusFilter);
            } else {
                filterFoodsInAllTab(searchTerm, statusFilter);
            }
        }

        function filterFoodsInSelectedTab(searchTerm, statusFilter) {
            const activeCategory = document.querySelector('.category-sidebar-btn.active').getAttribute('data-category');
            let foodCards;

            if (activeCategory === 'all') {
                foodCards = document.querySelectorAll('#foods-all .food-card');
            } else {
                foodCards = document.querySelectorAll(`#foods-category-${activeCategory} .food-card`);
            }

            let visibleCount = 0;

            foodCards.forEach(card => {
                const foodTitle = card.querySelector('h3').textContent.toLowerCase();
                const foodDescription = card.querySelector('p').textContent.toLowerCase();
                const foodStatus = card.getAttribute('data-status');

                const matchesSearch = foodTitle.includes(searchTerm) || foodDescription.includes(searchTerm);
                const matchesStatus = statusFilter === 'all' || foodStatus === statusFilter;

                if (matchesSearch && matchesStatus) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            showNoResultsMessage(activeCategory, visibleCount === 0);
        }

        function filterFoodsInAllTab(searchTerm, statusFilter) {
            const foodCards = document.querySelectorAll('#all-foods-container .food-card');
            let visibleCount = 0;

            foodCards.forEach(card => {
                const foodTitle = card.querySelector('h3').textContent.toLowerCase();
                const foodDescription = card.querySelector('p').textContent.toLowerCase();
                const foodStatus = card.getAttribute('data-status');

                const matchesSearch = foodTitle.includes(searchTerm) || foodDescription.includes(searchTerm);
                const matchesStatus = statusFilter === 'all' || foodStatus === statusFilter;

                if (matchesSearch && matchesStatus) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            showNoResultsMessage('all-foods', visibleCount === 0);
        }

        function showNoResultsMessage(sectionId, show) {
            let messageElement;

            if (sectionId === 'all-foods') {
                messageElement = document.querySelector('#all-foods-container .no-results-message');
            } else {
                const section = sectionId === 'all' ?
                    document.getElementById('foods-all') :
                    document.getElementById(`foods-category-${sectionId}`);
                messageElement = section?.querySelector('.no-results-message');
            }

            if (show && !messageElement) {
                messageElement = document.createElement('div');
                messageElement.className = 'no-results-message col-span-full text-center py-12';
                messageElement.innerHTML = `
                    <i class="fas fa-search text-4xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500 text-lg">نتیجه‌ای یافت نشد</p>
                    <p class="text-gray-400 text-sm mt-2">لطفاً عبارت جستجو یا فیلتر وضعیت را تغییر دهید</p>
                `;

                if (sectionId === 'all-foods') {
                    document.getElementById('all-foods-container').appendChild(messageElement);
                } else {
                    const section = sectionId === 'all' ?
                        document.getElementById('foods-all') :
                        document.getElementById(`foods-category-${sectionId}`);
                    const foodGrid = section?.querySelector('.food-grid');
                    if (foodGrid) {
                        foodGrid.appendChild(messageElement);
                    }
                }
            } else if (!show && messageElement) {
                messageElement.remove();
            }
        }

        // توابع اصلی برای عملیات غذاها
        async function toggleFoodStatus(foodId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/foods/${foodId}/toggle/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در تغییر وضعیت غذا');
            }
        }

        async function deleteFood(foodId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/foods/${foodId}/delete/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    const foodCard = document.querySelector(`[data-food-id="${foodId}"]`);
                    if (foodCard) {
                        foodCard.remove();
                    }
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در حذف غذا');
            }
        }

        async function toggleMenuCategoryStatus(categoryId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/menu-categories/${categoryId}/toggle/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در تغییر وضعیت دسته‌بندی');
            }
        }

        async function deleteMenuCategory(categoryId) {
            try {
                const response = await fetch(`/panel/${restaurantSlug}/menu-categories/${categoryId}/delete/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در حذف دسته‌بندی');
            }
        }

        async function loadFoodData(foodId) {
            try {
                document.getElementById('modal-title').textContent = 'ویرایش غذا';
                document.getElementById('food-id').value = foodId;

                const foodCard = document.querySelector(`[data-food-id="${foodId}"]`);
                if (foodCard) {
                    document.getElementById('food-title').value = foodCard.querySelector('h3').textContent;
                    document.getElementById('food-description').value = foodCard.querySelector('p').textContent;

                    const priceText = foodCard.querySelector('.font-bold').textContent;
                    const price = priceText.replace(/[^0-9]/g, '');
                    document.getElementById('food-price').value = price;

                    const prepTime = foodCard.querySelector('.fa-clock').parentElement.textContent.replace(/[^0-9]/g, '');
                    document.getElementById('food-preparation-time').value = prepTime;

                    const isActive = foodCard.getAttribute('data-status') === 'active';
                    document.getElementById('food-active').checked = isActive;

                    const categoryName = foodCard.querySelector('.fa-tag').parentElement.textContent.trim();
                    const categorySelect = document.getElementById('food-category');
                    for (let option of categorySelect.options) {
                        if (option.text === categoryName) {
                            $('.select2-category').val(option.value).trigger('change');
                            break;
                        }
                    }
                }

                document.getElementById('food-modal').style.display = 'flex';
            } catch (error) {
                showNotification('خطا در بارگذاری اطلاعات غذا');
            }
        }

        // توابع ارسال فرم
        async function submitFoodForm(form) {
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const loading = form.querySelector('.loading');

            submitBtn.disabled = true;
            loading?.classList.remove('hidden');

            try {
                const foodId = document.getElementById('food-id').value;
                const url = foodId ?
                    `/panel/${restaurantSlug}/foods/${foodId}/update/` :
                    `/panel/${restaurantSlug}/foods/add/`;

                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    form.closest('.modal').style.display = 'none';
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message || 'خطا در ذخیره غذا');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('خطا در ارسال اطلاعات');
            } finally {
                submitBtn.disabled = false;
                loading?.classList.add('hidden');
            }
        }

        async function submitCategoryForm(form) {
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const loading = form.querySelector('.loading');

            submitBtn.disabled = true;
            loading?.classList.remove('hidden');

            try {
                const response = await fetch(`/panel/${restaurantSlug}/menu-categories/add/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    form.closest('.modal').style.display = 'none';
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در ارسال اطلاعات');
            } finally {
                submitBtn.disabled = false;
                loading?.classList.add('hidden');
            }
        }

        async function submitRestaurantForm(form) {
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const loading = form.querySelector('.loading');

            submitBtn.disabled = true;
            loading?.classList.remove('hidden');

            try {
                const response = await fetch(`/panel/${restaurantSlug}/settings/update/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(result.message);
                    form.closest('.modal').style.display = 'none';
                } else {
                    showNotification(result.message);
                }
            } catch (error) {
                showNotification('خطا در ارسال اطلاعات');
            } finally {
                submitBtn.disabled = false;
                loading?.classList.add('hidden');
            }
        }

        // نمایش نوتیفیکیشن
        function showNotification(message, type = 'success') {
            const existingNotification = document.querySelector('.notification');
            if (existingNotification) {
                existingNotification.remove();
            }

            const notification = document.createElement('div');
            notification.className = `notification fixed top-20 left-1/2 transform -translate-x-1/2 ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white px-4 py-2 rounded-lg shadow-lg z-50 text-sm`;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => notification.remove(), 3000);
        }

        // ==================== بخش مدیریت انتخاب چندین دسته‌بندی ====================

        // لود درخت دسته‌بندی‌ها
        async function loadCategoryTree() {
            try {
                const container = document.getElementById('category-tree-container');
                container.innerHTML = `
                    <div class="text-center py-8">
                        <div class="loading mx-auto"></div>
                        <p class="text-gray-500 mt-2">در حال بارگذاری دسته‌بندی‌ها...</p>
                    </div>
                `;

                const response = await fetch(`/panel/${restaurantSlug}/categories/tree/`);
                const result = await response.json();

                if (result.success) {
                    renderCategoryTree(result.categories);
                } else {
                    container.innerHTML = `
                        <div class="text-center py-8 text-red-500">
                            <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                            <p>خطا در بارگذاری دسته‌بندی‌ها</p>
                            <p class="text-sm mt-2">${result.message || 'لطفاً دوباره تلاش کنید'}</p>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error loading category tree:', error);
                const container = document.getElementById('category-tree-container');
                container.innerHTML = `
                    <div class="text-center py-8 text-red-500">
                        <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                        <p>خطا در اتصال به سرور</p>
                        <p class="text-sm mt-2">لطفاً اتصال اینترنت خود را بررسی کنید</p>
                    </div>
                `;
            }
        }

        // رندر درخت دسته‌بندی‌ها
        function renderCategoryTree(categories) {
            const container = document.getElementById('category-tree-container');

            if (!categories || categories.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-8 text-gray-500">
                        <i class="fas fa-folder-open text-2xl mb-2"></i>
                        <p>دسته‌بندی‌ای یافت نشد</p>
                        <p class="text-sm mt-2">هنوز هیچ دسته‌بندی در سیستم تعریف نشده است</p>
                    </div>
                `;
                return;
            }

            let html = '<div class="category-tree space-y-3">';

            categories.forEach(parent => {
                const hasChildren = parent.subcategories && parent.subcategories.length > 0;

                html += `
                    <div class="parent-category">
                        <div class="parent-header" data-parent-id="${parent.id}">
                            <div class="parent-title">
                                ${parent.image_url ?
                                    `<img src="${parent.image_url}" alt="${parent.title}" class="parent-image">` :
                                    `<div class="parent-image bg-blue-100 flex items-center justify-center">
                                        <i class="fas fa-folder text-blue-500"></i>
                                    </div>`
                                }
                                <span class="font-medium">${parent.title}</span>
                                ${hasChildren ? `<span class="category-badge">${parent.subcategories.length} زیردسته</span>` : ''}
                            </div>
                            ${hasChildren ?
                                `<i class="fas fa-chevron-down category-arrow"></i>` :
                                `<span class="text-xs text-gray-500 px-2">بدون زیردسته</span>`
                            }
                        </div>
                        ${hasChildren ? `
                            <div class="parent-content">
                                <div class="space-y-2">
                                    ${parent.subcategories.map(sub => {
                                        const isSelected = selectedCategories.has(sub.id.toString());
                                        return `
                                        <div class="subcategory-item ${isSelected ? 'selected' : ''}"
                                            data-category-id="${sub.id}"
                                            data-category-name="${sub.title}">
                                            ${sub.image_url ?
                                                `<img src="${sub.image_url}" alt="${sub.title}" class="subcategory-image">` :
                                                `<div class="subcategory-image bg-green-100 flex items-center justify-center">
                                                    <i class="fas fa-tag text-green-500 text-sm"></i>
                                                </div>`
                                            }
                                            <span class="flex-1 font-medium">${sub.title}</span>
                                            <span class="text-xs opacity-75">${sub.parent_title}</span>
                                            <i class="fas fa-check-circle ${isSelected ? 'opacity-100' : 'opacity-0'} transition-opacity"></i>
                                        </div>
                                    `}).join('')}
                                </div>
                            </div>
                        ` : `
                            <div class="parent-content">
                                <div class="no-subcategories">
                                    <i class="fas fa-info-circle mb-1"></i>
                                    <p>این دسته‌بندی زیرمجموعه‌ای ندارد</p>
                                </div>
                            </div>
                        `}
                    </div>
                `;
            });

            html += '</div>';
            container.innerHTML = html;

            attachCategoryEventListeners();
        }

        // attach event listeners
        function attachCategoryEventListeners() {
            // کلیک روی هدر دسته‌بندی مادر
            document.querySelectorAll('.parent-header').forEach(header => {
                header.addEventListener('click', function() {
                    const parentId = this.getAttribute('data-parent-id');
                    const content = this.nextElementSibling;
                    const arrow = this.querySelector('.category-arrow');

                    if (content && arrow) {
                        content.classList.toggle('expanded');
                        arrow.classList.toggle('expanded');
                        this.classList.toggle('active');
                    }
                });
            });

            // کلیک روی زیردسته‌ها
            document.querySelectorAll('.subcategory-item').forEach(item => {
                item.addEventListener('click', function() {
                    const categoryId = this.getAttribute('data-category-id');
                    const categoryName = this.getAttribute('data-category-name');

                    if (selectedCategories.has(categoryId)) {
                        selectedCategories.delete(categoryId);
                        this.classList.remove('selected');
                        this.querySelector('.fa-check-circle').classList.add('opacity-0');
                    } else {
                        selectedCategories.set(categoryId, categoryName);
                        this.classList.add('selected');
                        this.querySelector('.fa-check-circle').classList.remove('opacity-0');
                    }

                    updateSelectedCategoriesUI();
                });
            });

            // جستجوی دسته‌بندی‌ها
            const searchInput = document.getElementById('category-search');
            if (searchInput) {
                searchInput.addEventListener('input', function(e) {
                    const searchTerm = e.target.value.toLowerCase().trim();
                    filterCategories(searchTerm);
                });
            }
        }

        // فیلتر کردن دسته‌بندی‌ها
        function filterCategories(searchTerm) {
            const allParents = document.querySelectorAll('.parent-category');

            if (!searchTerm) {
                allParents.forEach(parent => {
                    parent.style.display = 'block';
                    const subItems = parent.querySelectorAll('.subcategory-item');
                    subItems.forEach(item => item.style.display = 'flex');
                });
                return;
            }

            allParents.forEach(parent => {
                const parentHeader = parent.querySelector('.parent-header');
                const parentText = parentHeader.textContent.toLowerCase();
                const subItems = parent.querySelectorAll('.subcategory-item');
                let hasVisibleItems = false;

                subItems.forEach(item => {
                    const itemText = item.textContent.toLowerCase();
                    if (itemText.includes(searchTerm)) {
                        item.style.display = 'flex';
                        hasVisibleItems = true;
                        const content = parent.querySelector('.parent-content');
                        const arrow = parent.querySelector('.category-arrow');
                        if (content && arrow) {
                            content.classList.add('expanded');
                            arrow.classList.add('expanded');
                            parentHeader.classList.add('active');
                        }
                    } else {
                        item.style.display = 'none';
                    }
                });

                if (parentText.includes(searchTerm) || hasVisibleItems) {
                    parent.style.display = 'block';
                } else {
                    parent.style.display = 'none';
                }
            });
        }

        // انتخاب همه دسته‌بندی‌ها
        function selectAllCategories() {
            document.querySelectorAll('.subcategory-item').forEach(item => {
                const categoryId = item.getAttribute('data-category-id');
                const categoryName = item.getAttribute('data-category-name');

                selectedCategories.set(categoryId, categoryName);
                item.classList.add('selected');
                item.querySelector('.fa-check-circle').classList.remove('opacity-0');
            });

            updateSelectedCategoriesUI();
        }

        // لغو انتخاب همه دسته‌بندی‌ها
        function deselectAllCategories() {
            selectedCategories.clear();
            document.querySelectorAll('.subcategory-item').forEach(item => {
                item.classList.remove('selected');
                item.querySelector('.fa-check-circle').classList.add('opacity-0');
            });

            updateSelectedCategoriesUI();
        }

        // به‌روزرسانی UI دسته‌بندی‌های انتخاب شده
        function updateSelectedCategoriesUI() {
            const selectedCount = selectedCategories.size;
            const infoElement = document.getElementById('selected-categories-info');
            const countElement = document.getElementById('selected-categories-count');
            const listElement = document.getElementById('selected-categories-list');
            const confirmBtn = document.getElementById('confirm-categories-btn');

            if (confirmBtn) {
                confirmBtn.disabled = selectedCount === 0;
            }

            if (infoElement) {
                if (selectedCount > 0) {
                    infoElement.classList.remove('hidden');
                    if (countElement) {
                        countElement.textContent = `${selectedCount} دسته‌بندی انتخاب شده`;
                    }
                } else {
                    infoElement.classList.add('hidden');
                }
            }

            if (listElement) {
                listElement.innerHTML = '';
                selectedCategories.forEach((name, id) => {
                    const tag = document.createElement('div');
                    tag.className = 'selected-category-tag';
                    tag.innerHTML = `
                        ${name}
                        <button type="button" onclick="removeSelectedCategory('${id}')">
                            <i class="fas fa-times text-xs"></i>
                        </button>
                    `;
                    listElement.appendChild(tag);
                });
            }
        }

        // حذف یک دسته‌بندی از لیست انتخاب شده
        function removeSelectedCategory(categoryId) {
            selectedCategories.delete(categoryId);

            const item = document.querySelector(`[data-category-id="${categoryId}"]`);
            if (item) {
                item.classList.remove('selected');
                item.querySelector('.fa-check-circle').classList.add('opacity-0');
            }

            updateSelectedCategoriesUI();
        }

        // تأیید و افزودن دسته‌بندی‌های انتخاب شده
        async function confirmAndAddCategories() {
            if (selectedCategories.size === 0) return;

            const btn = document.getElementById('confirm-categories-btn');
            if (!btn) return;

            const originalText = btn.innerHTML;
            btn.innerHTML = '<div class="loading"></div> در حال افزودن...';
            btn.disabled = true;

            try {
                const response = await fetch(`/panel/${restaurantSlug}/categories/quick-add-multiple/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        category_ids: Array.from(selectedCategories.keys())
                    })
                });

                const result = await response.json();

                if (result.success) {
                    showNotification('✅ ' + result.message);
                    document.getElementById('quick-category-modal').style.display = 'none';
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showNotification('❌ ' + result.message);
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }
            } catch (error) {
                console.error('Error adding categories:', error);
                showNotification('❌ خطا در افزودن دسته‌بندی‌ها');
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        // بستن با کلیک خارج
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });


// =// در admin33.js - کد کامل شخصی‌سازی

// بارگذاری غذاهای شخصی‌سازی شده
function loadCustomizedFoods() {
    console.log('بارگذاری غذاهای شخصی‌سازی شده...');

    const container = document.getElementById('customized-foods-container');
    if (!container) return;

    container.innerHTML = `
        <div class="col-span-full text-center py-12">
            <div class="loading mx-auto mb-4"></div>
            <p class="text-gray-500">در حال بارگذاری غذاهای شخصی‌سازی شده...</p>
        </div>
    `;

    fetch(`/panel/${restaurantSlug}/customized-foods/`)
        .then(response => {
            if (!response.ok) throw new Error('خطا در دریافت داده‌ها');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                renderCustomizedFoods(data.customized_foods);
            } else {
                showError('خطا در بارگذاری داده‌ها: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('خطا در ارتباط با سرور');
        });
}

// نمایش غذاهای شخصی‌سازی شده
function renderCustomizedFoods(foods) {
    const container = document.getElementById('customized-foods-container');

    if (!foods || foods.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-palette text-4xl text-gray-300 mb-4"></i>
                <p class="text-gray-500 text-lg">هنوز غذایی شخصی‌سازی نکرده‌اید</p>
                <button class="mt-4 bg-pink-500 hover:bg-pink-600 text-white px-6 py-2 rounded-lg transition-colors" onclick="openModal('customize-foods-modal')">
                    <i class="fas fa-palette ml-2"></i>
                    شروع شخصی‌سازی
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = foods.map(food => `
        <div class="food-card bg-white rounded-xl shadow-sm overflow-hidden border-l-4 ${food.is_active ? 'border-green-500' : 'border-gray-300'}">
            <div class="relative">
                <img src="${food.final_image || food.original_image || '/static/images/food-placeholder.jpg'}"
                     alt="${food.title}"
                     class="w-full h-48 object-cover">
                <div class="absolute top-3 left-3">
                    <span class="status-badge ${food.is_active ? 'status-active' : 'status-inactive'}">
                        ${food.is_active ? 'فعال' : 'غیرفعال'}
                    </span>
                </div>
                <div class="absolute top-3 right-3 bg-white rounded-full p-2 shadow-md">
                    <span class="font-bold ${food.custom_price ? 'text-pink-600' : 'text-green-600'}">
                        ${food.final_price ? food.final_price.toLocaleString() + ' تومان' : 'تعیین نشده'}
                    </span>
                </div>
                <div class="absolute bottom-3 left-3">
                    <span class="bg-pink-500 text-white text-xs px-2 py-1 rounded-full">
                        <i class="fas fa-palette ml-1"></i> شخصی‌سازی شده
                    </span>
                </div>
            </div>
            <div class="p-4">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-lg text-gray-800">${food.title}</h3>
                    <div class="flex gap-1">
                        <button class="toggle-custom-food-status text-${food.is_active ? 'orange' : 'green'}-500 hover:text-${food.is_active ? 'orange' : 'green'}-700 p-1 rounded"
                                data-food-id="${food.food_id}">
                            <i class="fas fa-power-off"></i>
                        </button>
                        <button class="reset-customization text-red-500 hover:text-red-700 p-1 rounded"
                                data-food-id="${food.food_id}">
                            <i class="fas fa-undo"></i>
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-3 p-3 bg-gray-50 rounded-lg">
                    <div class="text-center">
                        <p class="text-sm text-gray-600 mb-1">قیمت اصلی</p>
                        <p class="font-bold text-gray-700">${food.original_price ? food.original_price.toLocaleString() + ' تومان' : 'تعیین نشده'}</p>
                    </div>
                    <div class="text-center">
                        <p class="text-sm text-gray-600 mb-1">${food.custom_price ? 'قیمت کاستوم' : 'قیمت نهایی'}</p>
                        <p class="font-bold ${food.custom_price ? 'text-pink-600' : 'text-green-600'}">
                            ${food.final_price ? food.final_price.toLocaleString() + ' تومان' : 'تعیین نشده'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    // اضافه کردن event listener
    document.querySelectorAll('.toggle-custom-food-status').forEach(btn => {
        btn.addEventListener('click', function() {
            const foodId = this.getAttribute('data-food-id');
            toggleCustomFoodStatus(foodId);
        });
    });

    document.querySelectorAll('.reset-customization').forEach(btn => {
        btn.addEventListener('click', function() {
            const foodId = this.getAttribute('data-food-id');
            resetCustomization(foodId);
        });
    });
}

// تغییر وضعیت غذای شخصی‌سازی شده
function toggleCustomFoodStatus(foodId) {
    fetch(`/panel/${restaurantSlug}/toggle-custom-food/${foodId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            loadCustomizedFoods();
        } else {
            showError(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('خطا در ارتباط با سرور');
    });
}

// بازنشانی شخصی‌سازی
function resetCustomization(foodId) {
    if (!confirm('آیا از بازنشانی شخصی‌سازی این غذا اطمینان دارید؟')) {
        return;
    }

    fetch(`/panel/${restaurantSlug}/reset-customization/${foodId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            loadCustomizedFoods();
        } else {
            showError(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('خطا در ارتباط با سرور');
    });
}

// تأیید شخصی‌سازی غذاها
// تأیید شخصی‌سازی غذاها
// تأیید شخصی‌سازی غذاها - نسخه دیباگ
function confirmCustomization() {
    console.log('=== شروع فرآیند شخصی‌سازی ===');

    const formData = new FormData();
    const customizedFoods = [];
    let hasChanges = false;

    // جمع‌آوری داده‌ها با لاگ دقیق
    document.querySelectorAll('.customize-food-item').forEach((item, index) => {
        const priceInput = item.querySelector('.custom-price-input');
        const imageInput = item.querySelector('.custom-image-input');

        if (priceInput) {
            const foodId = priceInput.getAttribute('data-food-id');
            const originalPrice = parseInt(priceInput.getAttribute('data-original-price')) || 0;
            const newPrice = parseInt(priceInput.value) || 0;

            console.log(`غذا #${index + 1}:`, {
                foodId: foodId,
                originalPrice: originalPrice,
                newPrice: newPrice,
                hasImage: imageInput && imageInput.files[0] ? true : false
            });

            // بررسی تغییرات
            const hasPriceChange = newPrice !== originalPrice;
            const hasImageChange = imageInput && imageInput.files[0];

            if (hasPriceChange || hasImageChange) {
                const customization = {
                    food_id: parseInt(foodId),
                    custom_price: newPrice
                };

                customizedFoods.push(customization);
                hasChanges = true;

                console.log(`✅ تغییرات برای غذا ${foodId} ثبت شد:`, customization);

                // اضافه کردن تصویر
                if (hasImageChange) {
                    formData.append(`image_${foodId}`, imageInput.files[0]);
                    console.log(`📸 تصویر برای غذا ${foodId} اضافه شد`);
                }
            } else {
                console.log(`➖ هیچ تغییری برای غذا ${foodId}`);
            }
        }
    });

    console.log('📊 جمع‌بندی تغییرات:', {
        totalFoods: document.querySelectorAll('.customize-food-item').length,
        customizedFoods: customizedFoods.length,
        customizedFoodsList: customizedFoods
    });

    if (!hasChanges) {
        console.log('⚠️ هیچ تغییری برای ذخیره کردن وجود ندارد');
        showWarning('هیچ تغییری برای ذخیره کردن وجود ندارد');
        return;
    }

    // اضافه کردن داده‌های JSON
    formData.append('customizations', JSON.stringify(customizedFoods));
    formData.append('restaurant_slug', restaurantSlug);

    // برای دیباگ: نمایش داده‌های ارسالی
    console.log('🚀 داده‌های ارسالی به سرور:', {
        customizedFoods: customizedFoods,
        formDataEntries: Array.from(formData.entries())
    });

    // نمایش لودینگ
    const confirmBtn = document.getElementById('confirm-customization-btn');
    const originalText = confirmBtn.innerHTML;
    confirmBtn.innerHTML = '<div class="loading mx-auto"></div> در حال ذخیره...';
    confirmBtn.disabled = true;

    // ارسال به سرور
    fetch(`/panel/${restaurantSlug}/bulk-customize-foods/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => {
        console.log('📨 پاسخ سرور دریافت شد - Status:', response.status);
        if (!response.ok) {
            throw new Error(`خطا در پاسخ سرور: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('✅ پاسخ کامل سرور:', data);

        if (data.success) {
            showSuccess(data.message);
            console.log('🎉 شخصی‌سازی با موفقیت انجام شد');
            closeModal('customize-foods-modal');

            // بارگذاری مجدد لیست غذاهای شخصی‌سازی شده
            if (typeof loadCustomizedFoods === 'function') {
                console.log('🔄 بارگذاری مجدد لیست غذاها...');
                loadCustomizedFoods();
            }
        } else {
            const errorMsg = data.message || (data.errors && data.errors.join(', ')) || 'خطای ناشناخته';
            console.error('❌ خطا از سرور:', errorMsg);
            showError('خطا در ذخیره: ' + errorMsg);
        }
    })
    .catch(error => {
        console.error('💥 خطا در ارسال درخواست:', error);
        showError('خطا در ارتباط با سرور: ' + error.message);
    })
    .finally(() => {
        confirmBtn.innerHTML = originalText;
        confirmBtn.disabled = false;
        console.log('=== پایان فرآیند شخصی‌سازی ===');
    });
}

// مدیریت تب‌ها و event listeners
document.addEventListener('DOMContentLoaded', function() {
    // مدیریت کلیک روی تب‌ها
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');

            // غیرفعال کردن همه تب‌ها
            document.querySelectorAll('.tab-btn').forEach(tab => {
                tab.classList.remove('active', 'text-blue-600', 'border-blue-600');
                tab.classList.add('text-gray-500');
            });

            // فعال کردن تب جاری
            this.classList.add('active', 'text-blue-600', 'border-blue-600');
            this.classList.remove('text-gray-500');

            // مخفی کردن همه محتواهای تب
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });

            // نمایش محتوای تب جاری
            const tabContent = document.getElementById(`${tabName}-tab`);
            if (tabContent) {
                tabContent.classList.add('active');

                // اگر تب شخصی‌سازی است، بارگذاری داده‌ها
                if (tabName === 'customize-foods') {
                    loadCustomizedFoods();
                }
            }
        });
    });

    // باز کردن مودال شخصی‌سازی
    const openCustomizeBtn = document.getElementById('open-customize-modal-btn');
    if (openCustomizeBtn) {
        openCustomizeBtn.addEventListener('click', function() {
            openModal('customize-foods-modal');
        });
    }

    // دکمه شخصی‌سازی در هدر
    const customizeHeaderBtn = document.getElementById('customize-foods-btn');
    if (customizeHeaderBtn) {
        customizeHeaderBtn.addEventListener('click', function() {
            document.querySelector('[data-tab="customize-foods"]').click();
        });
    }

    // FAB برای موبایل
    const fabCustomize = document.getElementById('fab-customize-foods');
    if (fabCustomize) {
        fabCustomize.addEventListener('click', function() {
            document.querySelector('[data-tab="customize-foods"]').click();
            closeFabMenu();
        });
    }

    // تأیید شخصی‌سازی
    const confirmBtn = document.getElementById('confirm-customization-btn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', confirmCustomization);
    }

    // پیش‌نمایش تصویر
    document.querySelectorAll('.custom-image-input').forEach(input => {
        input.addEventListener('change', function(e) {
            const foodId = this.getAttribute('data-food-id');
            const preview = document.getElementById(`preview-${foodId}`);

            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (preview) {
                        preview.src = e.target.result;
                        preview.classList.remove('hidden');
                    }
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    console.log('ماژول شخصی‌سازی غذا بارگذاری شد');
});

// توابع کمکی
function showSuccess(message) {
    alert('✅ ' + message);
}

function showError(message) {
    alert('❌ ' + message);
}

function showWarning(message) {
    alert('⚠️ ' + message);
}



 document.addEventListener('DOMContentLoaded', function() {
            // مدیریت تب‌ها
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const tabName = this.getAttribute('data-tab');

                    // غیرفعال کردن همه تب‌ها
                    document.querySelectorAll('.tab-btn').forEach(tab => {
                        tab.classList.remove('active', 'text-blue-600', 'border-blue-600');
                        tab.classList.add('text-gray-500');
                    });

                    // فعال کردن تب جاری
                    this.classList.add('active', 'text-blue-600', 'border-blue-600');
                    this.classList.remove('text-gray-500');

                    // مخفی کردن همه محتواهای تب
                    document.querySelectorAll('.tab-content').forEach(content => {
                        content.classList.remove('active');
                    });

                    // نمایش محتوای تب جاری
                    const tabContent = document.getElementById(`${tabName}-tab`);
                    if (tabContent) {
                        tabContent.classList.add('active');
                    }
                });
            });

            // باز کردن مودال شخصی‌سازی
            const openCustomizeBtn = document.getElementById('open-customize-modal-btn');
            if (openCustomizeBtn) {
                openCustomizeBtn.addEventListener('click', function() {
                    const modal = document.getElementById('customize-foods-modal');
                    if (modal) {
                        modal.classList.add('active');
                    }
                });
            }

            // دکمه شخصی‌سازی در هدر
            const customizeHeaderBtn = document.getElementById('customize-foods-btn');
            if (customizeHeaderBtn) {
                customizeHeaderBtn.addEventListener('click', function() {
                    // فعال کردن تب شخصی‌سازی
                    document.querySelectorAll('.tab-btn').forEach(tab => {
                        tab.classList.remove('active', 'text-blue-600', 'border-blue-600');
                        tab.classList.add('text-gray-500');
                    });

                    const customizeTab = document.querySelector('[data-tab="customize-foods"]');
                    if (customizeTab) {
                        customizeTab.classList.add('active', 'text-blue-600', 'border-blue-600');
                        customizeTab.classList.remove('text-gray-500');
                    }

                    document.querySelectorAll('.tab-content').forEach(content => {
                        content.classList.remove('active');
                    });

                    const customizeContent = document.getElementById('customize-foods-tab');
                    if (customizeContent) {
                        customizeContent.classList.add('active');
                    }
                });
            }

            // FAB برای موبایل
            const fabMain = document.getElementById('fab-main');
            const fabMenu = document.getElementById('fab-menu');
            if (fabMain && fabMenu) {
                fabMain.addEventListener('click', function() {
                    fabMenu.classList.toggle('active');
                });
            }

            const fabCustomize = document.getElementById('fab-customize-foods');
            if (fabCustomize) {
                fabCustomize.addEventListener('click', function() {
                    // فعال کردن تب شخصی‌سازی
                    document.querySelectorAll('.tab-btn').forEach(tab => {
                        tab.classList.remove('active', 'text-blue-600', 'border-blue-600');
                        tab.classList.add('text-gray-500');
                    });

                    const customizeTab = document.querySelector('[data-tab="customize-foods"]');
                    if (customizeTab) {
                        customizeTab.classList.add('active', 'text-blue-600', 'border-blue-600');
                        customizeTab.classList.remove('text-gray-500');
                    }

                    document.querySelectorAll('.tab-content').forEach(content => {
                        content.classList.remove('active');
                    });

                    const customizeContent = document.getElementById('customize-foods-tab');
                    if (customizeContent) {
                        customizeContent.classList.add('active');
                    }

                    // بستن منوی FAB
                    if (fabMenu) {
                        fabMenu.classList.remove('active');
                    }
                });
            }

            // پیش‌نمایش تصویر در مودال شخصی‌سازی
            document.querySelectorAll('.custom-image-input').forEach(input => {
                input.addEventListener('change', function(e) {
                    const foodId = this.getAttribute('data-food-id');
                    const preview = document.getElementById(`preview-${foodId}`);

                    if (this.files && this.files[0]) {
                        const reader = new FileReader();

                        reader.onload = function(e) {
                            if (preview) {
                                preview.src = e.target.result;
                                preview.classList.remove('hidden');
                            }
                        }

                        reader.readAsDataURL(this.files[0]);
                    }
                });
            });

            // تأیید شخصی‌سازی
            const confirmBtn = document.getElementById('confirm-customization-btn');
            if (confirmBtn) {
                confirmBtn.addEventListener('click', function() {
                    const customizedFoods = [];

                    document.querySelectorAll('.customize-food-item').forEach(item => {
                        const priceInput = item.querySelector('.custom-price-input');
                        const imageInput = item.querySelector('.custom-image-input');

                        if (priceInput) {
                            const foodId = priceInput.getAttribute('data-food-id');
                            const newPrice = priceInput.value;
                            const originalPrice = priceInput.getAttribute('data-original-price');
                            const imageFile = imageInput ? imageInput.files[0] : null;

                            // فقط اگر تغییری ایجاد شده باشد
                            if (newPrice !== originalPrice || imageFile) {
                                customizedFoods.push({
                                    foodId: foodId,
                                    newPrice: newPrice,
                                    imageFile: imageFile
                                });
                            }
                        }
                    });

                    if (customizedFoods.length === 0) {
                        alert('هیچ تغییری اعمال نکرده‌اید!');
                        return;
                    }

                    // ارسال داده‌ها به سرور
                    const formData = new FormData();
                    formData.append('restaurant_slug', restaurantSlug);
                    formData.append('customized_foods', JSON.stringify(customizedFoods));
                    formData.append('csrfmiddlewaretoken', csrfToken);

                    // اضافه کردن فایل‌های تصویر
                    customizedFoods.forEach((food, index) => {
                        if (food.imageFile) {
                            formData.append(`image_${food.foodId}`, food.imageFile);
                        }
                    });

                    fetch('/api/customize-foods/', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('تغییرات با موفقیت ذخیره شدند!');
                            location.reload();
                        } else {
                            alert('خطا در ذخیره تغییرات: ' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('خطا در ارتباط با سرور');
                    });
                });
            }

            // مدیریت بستن مودال‌ها
            document.querySelectorAll('.close-modal').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.modal').forEach(modal => {
                        modal.classList.remove('active');
                    });
                });
            });

            // بستن مودال با کلیک خارج از آن
            document.addEventListener('click', function(e) {
                if (e.target.classList.contains('modal')) {
                    e.target.classList.remove('active');
                }
            });
        });



