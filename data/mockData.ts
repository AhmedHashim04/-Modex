import { Product, Category } from '../types';

export const categories: Category[] = [
  {
    id: 'gifts',
    name: 'Gifts',
    nameAr: 'هدايا',
    icon: 'Gift',
    subcategories: [
      { id: 'birthday', name: 'Birthday', nameAr: 'عيد ميلاد', icon: 'Cake' },
      { id: 'wedding', name: 'Wedding', nameAr: 'زفاف', icon: 'Heart' },
      { id: 'anniversary', name: 'Anniversary', nameAr: 'ذكرى سنوية', icon: 'Calendar' }
    ]
  },
  {
    id: 'toys',
    name: 'Toys',
    nameAr: 'ألعاب',
    icon: 'Gamepad2',
    subcategories: [
      { id: 'educational', name: 'Educational', nameAr: 'تعليمية', icon: 'BookOpen' },
      { id: 'outdoor', name: 'Outdoor', nameAr: 'خارجية', icon: 'TreePine' },
      { id: 'electronic', name: 'Electronic', nameAr: 'إلكترونية', icon: 'Zap' }
    ]
  },
  {
    id: 'clothing',
    name: 'Clothing',
    nameAr: 'ملابس',
    icon: 'Shirt',
    subcategories: [
      { id: 'men', name: 'Men', nameAr: 'رجالي', icon: 'User' },
      { id: 'women', name: 'Women', nameAr: 'نسائي', icon: 'UserCheck' },
      { id: 'kids', name: 'Kids', nameAr: 'أطفال', icon: 'Baby' }
    ]
  },
  {
    id: 'shoes',
    name: 'Shoes',
    nameAr: 'أحذية',
    icon: 'Footprints',
    subcategories: [
      { id: 'sports', name: 'Sports', nameAr: 'رياضية', icon: 'Activity' },
      { id: 'formal', name: 'Formal', nameAr: 'رسمية', icon: 'Briefcase' },
      { id: 'casual', name: 'Casual', nameAr: 'كاجوال', icon: 'Coffee' }
    ]
  },
  {
    id: 'accessories',
    name: 'Accessories',
    nameAr: 'إكسسوارات',
    icon: 'Watch',
    subcategories: [
      { id: 'jewelry', name: 'Jewelry', nameAr: 'مجوهرات', icon: 'Gem' },
      { id: 'bags', name: 'Bags', nameAr: 'حقائب', icon: 'ShoppingBag' },
      { id: 'watches', name: 'Watches', nameAr: 'ساعات', icon: 'Clock' }
    ]
  },
  {
    id: 'perfumes',
    name: 'Perfumes',
    nameAr: 'عطور',
    icon: 'Spray',
    subcategories: [
      { id: 'men-perfumes', name: 'Men', nameAr: 'رجالي', icon: 'User' },
      { id: 'women-perfumes', name: 'Women', nameAr: 'نسائي', icon: 'UserCheck' },
      { id: 'unisex', name: 'Unisex', nameAr: 'للجنسين', icon: 'Users' }
    ]
  }
];

export const sampleProducts: Product[] = [
  {
    id: '1',
    name: 'Luxury Watch',
    nameAr: 'ساعة فاخرة',
    description: 'Premium stainless steel watch with automatic movement',
    descriptionAr: 'ساعة من الستانلس ستيل الفاخر بحركة أوتوماتيكية',
    price: 299.99,
    discountPrice: 249.99,
    category: 'accessories',
    categoryAr: 'إكسسوارات',
    images: ['https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg'],
    featured: true,
    inStock: true,
    rating: 4.8,
    reviews: 124,
    color: 'Silver',
    weight: 150
  },
  {
    id: '2',
    name: 'Gaming Console',
    nameAr: 'جهاز ألعاب',
    description: 'Next-generation gaming console with 4K support',
    descriptionAr: 'جهاز ألعاب من الجيل التالي مع دعم 4K',
    price: 599.99,
    category: 'toys',
    categoryAr: 'ألعاب',
    images: ['https://images.pexels.com/photos/442576/pexels-photo-442576.jpeg'],
    featured: true,
    inStock: true,
    rating: 4.9,
    reviews: 89,
    dimensions: { length: 30, width: 25, height: 8 },
    weight: 2500
  },
  {
    id: '3',
    name: 'Designer Handbag',
    nameAr: 'حقيبة يد مصممة',
    description: 'Elegant leather handbag perfect for any occasion',
    descriptionAr: 'حقيبة يد أنيقة من الجلد مثالية لأي مناسبة',
    price: 199.99,
    discountPrice: 159.99,
    category: 'accessories',
    categoryAr: 'إكسسوارات',
    images: ['https://images.pexels.com/photos/904350/pexels-photo-904350.jpeg'],
    inStock: true,
    rating: 4.7,
    reviews: 156,
    color: 'Brown',
    dimensions: { length: 35, width: 12, height: 25 },
    weight: 800
  },
  {
    id: '4',
    name: 'Premium Perfume',
    nameAr: 'عطر فاخر',
    description: 'Luxury fragrance with long-lasting scent',
    descriptionAr: 'عطر فاخر برائحة تدوم طويلاً',
    price: 149.99,
    category: 'perfumes',
    categoryAr: 'عطور',
    images: ['https://images.pexels.com/photos/965989/pexels-photo-965989.jpeg'],
    featured: true,
    inStock: true,
    rating: 4.6,
    reviews: 78,
    dimensions: { length: 5, width: 5, height: 12 },
    weight: 200
  },
  {
    id: '5',
    name: 'Running Shoes',
    nameAr: 'حذاء رياضي',
    description: 'Comfortable running shoes with advanced cushioning',
    descriptionAr: 'حذاء رياضي مريح مع وسائد متقدمة',
    price: 129.99,
    discountPrice: 99.99,
    category: 'shoes',
    categoryAr: 'أحذية',
    images: ['https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg'],
    inStock: true,
    rating: 4.5,
    reviews: 203,
    color: 'Black/White',
    weight: 350
  },
  {
    id: '6',
    name: 'Casual T-Shirt',
    nameAr: 'تيشيرت كاجوال',
    description: 'Comfortable cotton t-shirt for everyday wear',
    descriptionAr: 'تيشيرت قطني مريح للارتداء اليومي',
    price: 29.99,
    category: 'clothing',
    categoryAr: 'ملابس',
    images: ['https://images.pexels.com/photos/769732/pexels-photo-769732.jpeg'],
    inStock: true,
    rating: 4.3,
    reviews: 89,
    color: 'Navy Blue',
    weight: 180
  }
];