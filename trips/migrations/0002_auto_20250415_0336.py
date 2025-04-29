from django.db import migrations

def create_activities(apps, schema_editor):
    Activity = apps.get_model('trips', 'Activity')

    activity_names = [
        "Hiking", "Beach", "Museum", "Shopping", "Nightlife",
        "Local Cuisine", "Historical Sites", "Snorkeling", "Art Galleries",
        "Live Music", "Nature Tours", "Skiing", "Surfing", "Amusement Parks",
        "Food Tours", "Boat Rides", "Camping", "Zoo", "Aquarium", "Biking",
        "Kayaking", "Paddleboarding", "Fishing", "Spa Day", "Yoga Class",
        "Scuba Diving", "Horseback Riding", "Rock Climbing", "Skydiving",
        "ATV Tours", "Ziplining", "Helicopter Tours", "Farmers Market",
        "Botanical Gardens", "Theme Parks", "Trampoline Parks",
        "Go Kart Racing", "Escape Rooms", "Arcades", "Golfing", "Casino",
        "Ice Skating", "Snowboarding", "Sledding", "Tubing", "Haunted Tours",
        "Sunset Watching", "Stargazing", "Photography Walk", "Train Rides",
        "Festivals", "Dance Class", "Pottery Class", "Painting Class",
        "Lighthouse Visits", "Water Parks", "Boat Rentals", "Jet Skiing",
        "Cruise Excursions", "Mountain Biking", "Nature Photography",
        "Flea Markets", "Thrift Shopping", "Scenic Drives",
        "Street Performances"
    ]

    for name in activity_names:
        Activity.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_activities),
    ]
