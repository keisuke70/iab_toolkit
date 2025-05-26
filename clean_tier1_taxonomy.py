#!/usr/bin/env python3
"""
Clean the tier1_taxonomy.json file by removing unnecessary entries and fields.
"""

import json

# The clean data (from the attachment, but with unnecessary fields removed)
clean_data = [
  {
    "unique_id": "150",
    "name": "Attractions",
    "description": "Domain: Attractions. Main categories: Historic Site and Landmark Tours, Bars & Restaurants, Outdoor Activities, Theater Venues, Malls & Shopping Centers, Amusement and Theme Parks, Casinos & Gambling, Zoos & Aquariums, Nightclubs, Museums & Galleries",
    "tier_1": "Attractions"
  },
  {
    "unique_id": "1",
    "name": "Automotive",
    "description": "Domain: Automotive. Main categories: Auto Parts, Auto Body Styles, Auto Buying and Selling, Auto Recalls, Motorcycles, Auto Shows, Auto Safety, Auto Insurance, Auto Repair, Dash Cam Videos. Subcategories: Crossover, Certified Pre-Owned Cars, Auto Infotainment Technologies, Green Vehicles, Auto Navigation Systems, Auto Safety Technologies, Sedan, Microcar, Station Wagon, SUV, Off-Road Vehicles, Pickup Trucks, Van, Hatchback, Concept Cars",
    "tier_1": "Automotive"
  },
  {
    "unique_id": "42",
    "name": "Books and Literature",
    "description": "Domain: Books and Literature. Main categories: Art and Photography, Poetry, Comics and Graphic Novels, Fiction",
    "tier_1": "Books and Literature"
  },
  {
    "unique_id": "52",
    "name": "Business and Finance",
    "description": "Domain: Business and Finance. Main categories: Industries, Business, Economy. Subcategories: Hospitality Industry, Defense Industry, Information Services Industry, Manufacturing Industry, Business Utilities, Publishing Industry, Gasoline Prices, Civil Engineering Industry, Metals Industry, Power and Energy Industry, Telecommunications Industry, Advertising Industry, Automotive Industry, Entertainment Industry, Business I.T.. Specific topics: Private Equity, Sale & Lease Back, Mergers and Acquisitions, Angel Investment, Bankruptcy, Recalls, Venture Capital, Debt Factoring & Invoice Discounting, Business Loans",
    "tier_1": "Business and Finance"
  },
  {
    "unique_id": "123",
    "name": "Careers",
    "description": "Domain: Careers. Main categories: Career Planning, Career Advice, Apprenticeships, Remote Working, Vocational Training, Job Search. Subcategories: Resume Writing and Advice, Job Fairs",
    "tier_1": "Careers"
  },
  {
    "unique_id": "80DV8O",
    "name": "Communication",
    "description": "Domain: Communication",
    "tier_1": "Communication"
  },
  {
    "unique_id": "380",
    "name": "Crime",
    "description": "Domain: Crime",
    "tier_1": "Crime"
  },
  {
    "unique_id": "381",
    "name": "Disasters",
    "description": "Domain: Disasters",
    "tier_1": "Disasters"
  },
  {
    "unique_id": "132",
    "name": "Education",
    "description": "Domain: Education. Main categories: Homework and Study, Educational Assessment, Early Childhood Education, Secondary Education, Homeschooling, Online Education, Private School, College Education, Adult Education, Primary Education. Subcategories: Postgraduate Education, Standardized Testing, Undergraduate Education, College Planning. Specific topics: Professional School",
    "tier_1": "Education"
  },
  {
    "unique_id": "JLBCU7",
    "name": "Entertainment",
    "description": "Domain: Entertainment. Main categories: Religious (Music and Audio), Oldies/Adult Standards, Movies, Classic Hits, Urban Contemporary Music, Dance and Electronic Music, Adult Album Alternative, Variety (Music and Audio), Music, Songwriters/Folk. Subcategories: Hard Rock, Urban AC Music, Album-oriented Rock, Soft AC Music, Alternative Rock, Soft Rock, Classic Rock",
    "tier_1": "Entertainment"
  },
  {
    "unique_id": "8VZQHL",
    "name": "Events",
    "description": "Domain: Events. Main categories: Fan Conventions, Business Expos & Conferences, Awards Shows",
    "tier_1": "Events"
  },
  {
    "unique_id": "186",
    "name": "Family and Relationships",
    "description": "Domain: Family and Relationships. Main categories: Dating, Marriage and Civil Unions, Parenting, Single Life, Bereavement, Divorce, Eldercare. Subcategories: Special Needs Kids, Internet Safety, Daycare and Pre-School, Parenting Babies and Toddlers, Adoption and Fostering, Parenting Children Aged 4-11, Parenting Teens",
    "tier_1": "Family and Relationships"
  },
  {
    "unique_id": "201",
    "name": "Fine Art",
    "description": "Domain: Fine Art. Main categories: Dance, Design, Modern Art, Fine Art Photography, Digital Arts, Costume, Opera, Theater",
    "tier_1": "Fine Art"
  },
  {
    "unique_id": "210",
    "name": "Food & Drink",
    "description": "Domain: Food & Drink. Main categories: World Cuisines, Vegan Diets, Vegetarian Diets, Food Allergies, Barbecues and Grilling, Dining Out, Non-Alcoholic Beverages, Cooking, Alcoholic Beverages, Food Movements",
    "tier_1": "Food & Drink"
  },
  {
    "unique_id": "VKIV56",
    "name": "Genres",
    "description": "Domain: Genres. Main categories: Comedy, Drama, Family/Children, Young Adult, Sports Radio, History, Mystery, Factual, Special Interest (Indie/Art House), Animation & Anime. Subcategories: Public Radio",
    "tier_1": "Genres"
  },
  {
    "unique_id": "223",
    "name": "Healthy Living",
    "description": "Domain: Healthy Living. Main categories: Nutrition, Women's Health, Senior Health, Fitness and Exercise, Weight Loss, Wellness, Children's Health, Men's Health. Subcategories: Alternative Medicine, Smoking Cessation, Participant Sports, Physical Therapy, Running and Jogging. Specific topics: Holistic Health, Herbs and Supplements",
    "tier_1": "Healthy Living"
  },
  {
    "unique_id": "239",
    "name": "Hobbies & Interests",
    "description": "Domain: Hobbies & Interests. Main categories: Model Toys, Paranormal Phenomena, Workshops and Classes, Musical Instruments, Radio Control, Cigars, Arts and Crafts, Antiquing and Antiques, Beekeeping, Genealogy and Ancestry. Subcategories: Roleplaying Games, Comic Books, Photography, Beadwork, Woodworking, Needlework, Painting, Screenwriting, Freelance Writing, Card Games, Drawing and Sketching, Jewelry Making, Video Production, Candle and Soap Making, Audio Production",
    "tier_1": "Hobbies & Interests"
  },
  {
    "unique_id": "1KXCLD",
    "name": "Holidays",
    "description": "Domain: Holidays. Main categories: National & Civic Holidays",
    "tier_1": "Holidays"
  },
  {
    "unique_id": "274",
    "name": "Home & Garden",
    "description": "Domain: Home & Garden. Main categories: Landscaping, Home Security, Interior Decorating, Gardening, Home Entertaining, Outdoor Decorating, Indoor Environmental Quality, Home Improvement, Remodeling & Construction, Smart Home",
    "tier_1": "Home & Garden"
  },
  {
    "unique_id": "383",
    "name": "Law",
    "description": "Domain: Law",
    "tier_1": "Law"
  },
  {
    "unique_id": "WQC6HR",
    "name": "Maps & Navigation",
    "description": "Domain: Maps & Navigation",
    "tier_1": "Maps & Navigation"
  },
  {
    "unique_id": "286",
    "name": "Medical Health",
    "description": "Domain: Medical Health. Main categories: Diseases and Conditions, Vaccines, Surgery, Pharmaceutical Drugs, Medical Tests, Cosmetic Medical Services. Subcategories: Blood Disorders, Cold and Flu, Sexual Health, Digestive Disorders, Skin and Dermatology, Dental Health, Mental Health, Brain and Nervous System Disorders, Injuries, Cancer, Infectious Diseases, Substance Abuse, Endocrine and Metabolic Diseases, Diabetes, Allergies. Specific topics: Sexual Conditions, Thyroid Disorders, Pregnancy, First Aid, Birth Control, Menopause, Hormonal Disorders, Infertility",
    "tier_1": "Medical Health"
  },
  {
    "unique_id": "163",
    "name": "Personal Celebrations & Life Events",
    "description": "Domain: Personal Celebrations & Life Events. Main categories: Birth, Anniversary, Bachelor Party, Bachelorette Party, Graduation, Prom, Wedding, Birthday, Funeral, Baby Shower",
    "tier_1": "Personal Celebrations & Life Events"
  },
  {
    "unique_id": "391",
    "name": "Personal Finance",
    "description": "Domain: Personal Finance. Main categories: Personal Investing, Personal Debt, Financial Planning, Consumer Banking, Financial Assistance, Retirement Planning, Home Utilities, Insurance, Personal Taxes, Frugal Living. Subcategories: Hedge Funds, Student Loans, Phone Services, Travel Insurance, Home Insurance, Government Support and Welfare, Life Insurance, Health Insurance, Gas and Electric, Stocks and Bonds, Water Services, Motor Insurance, Home Financing, Personal Loans, Mutual Funds",
    "tier_1": "Personal Finance"
  },
  {
    "unique_id": "422",
    "name": "Pets",
    "description": "Domain: Pets. Main categories: Reptiles, Pet Supplies, Pet Adoptions, Fish and Aquariums, Cats, Birds, Dogs, Veterinary Medicine, Large Animals",
    "tier_1": "Pets"
  },
  {
    "unique_id": "386",
    "name": "Politics",
    "description": "Domain: Politics. Main categories: Elections, Civic affairs, Political Issues & policy",
    "tier_1": "Politics"
  },
  {
    "unique_id": "432",
    "name": "Pop Culture",
    "description": "Domain: Pop Culture. Main categories: Celebrity Relationships, Celebrity Style, Celebrity Families, Celebrity Pregnancy, Celebrity Homes, Celebrity Deaths, Celebrity Scandal, Humor and Satire",
    "tier_1": "Pop Culture"
  },
  {
    "unique_id": "W3CW2J",
    "name": "Productivity",
    "description": "Domain: Productivity",
    "tier_1": "Productivity"
  },
  {
    "unique_id": "441",
    "name": "Real Estate",
    "description": "Domain: Real Estate. Main categories: Developmental Sites, Apartments, Industrial Property, Houses, Real Estate Buying and Selling, Vacation Properties, Land and Farms, Hotel Properties, Office Property, Real Estate Renting and Leasing",
    "tier_1": "Real Estate"
  },
  {
    "unique_id": "453",
    "name": "Religion & Spirituality",
    "description": "Domain: Religion & Spirituality. Main categories: Judaism, Atheism, Agnosticism, Buddhism, Islam, Christianity, Sikhism, Astrology, Hinduism, Spirituality",
    "tier_1": "Religion & Spirituality"
  },
  {
    "unique_id": "464",
    "name": "Science",
    "description": "Domain: Science. Main categories: Geology, Physics, Genetics, Geography, Space and Astronomy, Weather, Biological Sciences, Chemistry, Environment",
    "tier_1": "Science"
  },
  {
    "unique_id": "v9i3On",
    "name": "Sensitive Topics",
    "description": "Domain: Sensitive Topics. Main categories: Arms & Ammunition, Death, Injury, or Military Conflict, Crime & Harmful Acts to Individuals, Society & Human Right Violations, Spam or Harmful Content, Terrorism, Debated Sensitive Social Issues, Hate Speech and Acts of Aggression, Adult & Explicit Sexual Content, Illegal Drugs, Tobacco, eCigarettes, Vaping, Alcohol, Online Piracy",
    "tier_1": "Sensitive Topics"
  },
  {
    "unique_id": "473",
    "name": "Shopping",
    "description": "Domain: Shopping. Main categories: Coupons and Discounts, Party Supplies and Decorations, Flower Shopping, Gifts and Greetings Cards, Holiday Shopping, Grocery Shopping, Children's Games and Toys, Household Supplies, Sales and Promotions, Lotteries and Scratchcards",
    "tier_1": "Shopping"
  },
  {
    "unique_id": "483",
    "name": "Sports",
    "description": "Domain: Sports. Main categories: Sports Equipment, Darts, Track and Field, Cycling, Australian Rules Football, Cheerleading, Extreme Sports, Tennis, Figure Skating, Walking. Subcategories: Canoeing and Kayaking, Climbing, College Football, Snowboarding, College Baseball, Surfing and Bodyboarding, Waterskiing and Wakeboarding, Winter Olympic Sports, Horse Racing, Paintball, Rugby League, Summer Olympic Sports, College Basketball, Scuba Diving, Motorcycle Sports",
    "tier_1": "Sports"
  },
  {
    "unique_id": "552",
    "name": "Style & Fashion",
    "description": "Domain: Style & Fashion. Main categories: Street Style, Children's Clothing, Women's Fashion, High Fashion, Personal Care, Body Art, Designer Clothing, Beauty, Fashion Trends, Men's Fashion. Subcategories: Women's Shoes and Footwear, Nail Care, Natural and Organic Beauty, Women's Clothing, Oral care, Perfume and Fragrance, Skin Care, Men's Shoes and Footwear, Deodorant and Antiperspirant, Makeup and Accessories, Men's Accessories, Shaving, Women's Accessories, Hair Care, Bath and Shower. Specific topics: Women's Handbags and Wallets, Women's Outerwear, Women's Hats and Scarves, Women's Glasses, Men's Sportswear, Women's Business Wear, Men's Outerwear, Men's Jewelry and Watches, Women's Intimates and Sleepwear, Men's Business Wear",
    "tier_1": "Style & Fashion"
  },
  {
    "unique_id": "596",
    "name": "Technology & Computing",
    "description": "Domain: Technology & Computing. Main categories: Computing, Virtual Reality, Consumer Electronics, Robotics, Artificial Intelligence, Augmented Reality. Subcategories: Smartphones, Data Storage and Warehousing, Programming Languages, Internet, Tablets and E-readers, Wearable Technology, Cameras and Camcorders, Computer Networking, Computer Peripherals, Home Entertainment Systems, Laptops, Information and Network Security, Desktops, Computer Software and Applications. Specific topics: Photo Editing Software, Video Software, Internet for Beginners, Social Networking, Computer Animation, Web Conferencing, Cloud Computing, Shareware and Freeware, Email, Desktop Publishing",
    "tier_1": "Technology & Computing"
  },
  {
    "unique_id": "653",
    "name": "Travel",
    "description": "Domain: Travel. Main categories: Travel Preparation and Advice, Travel Type, Travel Locations, Travel Accessories. Subcategories: South America Travel, Polar Travel, Australia and Oceania Travel, Africa Travel, Family Travel, Beach Travel, Camping, Spas, Road Trips, North America Travel, Europe Travel, Adventure Travel, Day Trips, Air Travel, Bed & Breakfasts",
    "tier_1": "Travel"
  },
  {
    "unique_id": "680",
    "name": "Video Gaming",
    "description": "Domain: Video Gaming. Main categories: Video Game Genres, Mobile Games, Console Games, PC Games, eSports. Subcategories: Family Video Games, MMOs, Horror Video Games, Sports Video Games, Educational Video Games, Simulation Video Games, Puzzle Video Games, Casual Games, Music and Party Video Games, Adult Video Games, Strategy Video Games, Racing Video Games, Adventure Video Games, Role-Playing Video Games, Action Video Games",
    "tier_1": "Video Gaming"
  },
  {
    "unique_id": "389",
    "name": "War and Conflicts",
    "description": "Domain: War and Conflicts",
    "tier_1": "War and Conflicts"
  }
]

def main():
    """Clean and save the tier1_taxonomy.json file."""
    
    # Write the clean data
    output_path = "iab_toolkit/data/tier1_taxonomy.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
    
    print("✅ TIER 1 TAXONOMY CLEANUP COMPLETE!")
    print("="*50)
    print(f"📊 Total domains: {len(clean_data)}")
    print("🧹 Removed:")
    print("  - Useless 'Tier 1' meta entry")
    print("  - tier_2, tier_3, tier_4 (always null)")
    print("  - child_count (unnecessary)")
    print("📋 Kept:")
    print("  - unique_id (for identification)")
    print("  - name (domain name)")
    print("  - description (rich content from taxonomy)")
    print("  - tier_1 (for validation)")
    print(f"\n📄 File saved: {output_path}")
    
    # Show key domains for verification
    print("\n🔍 Key domains for Style & Fashion vs Medical Health:")
    for domain in clean_data:
        if domain['name'] in ['Style & Fashion', 'Medical Health']:
            print(f"\n{domain['name']}:")
            print(f"  Description: {domain['description'][:120]}...")

if __name__ == "__main__":
    main()
