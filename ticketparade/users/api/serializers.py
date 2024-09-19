from rest_framework import serializers

from ticketparade.users.models import User, Theater, TheaterSeat, BooekedTheaterSeat


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class TheaterSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ["name", "address", "city", "state", "zip_code", "phone", "email"]


class TheaterSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterSeat
        fields = ["theater_id", "seat_number", "is_available"]


class MovieSerialzer(serializers.Serializer):
    adult = serializers.BooleanField()
    backdrop_path = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField()
    poster_path = serializers.CharField()
    release_date = serializers.CharField()
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()


class BookTheaterSeatSerialzer(serializers.Serializer):
    theater_id = serializers.IntegerField()
    seat_ids = serializers.ListField(child=serializers.IntegerField())
    movie_id = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_theater_id(self, value):
        if not Theater.objects.filter(id=value).exists():
            raise serializers.ValidationError("Theater does not exist")
        return value

    def validate_seat_numbers(self, value):
        if not TheaterSeat.objects.filter(
            theater_id=self.initial_data.get("theater_id"),
            seat_id__in=value,
            is_available=True,
        ).exists():
            raise serializers.ValidationError("Seat not available")

        return value

    def create(self, validated_data):
        booked_seats = [
            BooekedTheaterSeat(
                theater_seat_id=seat_id,
                email=validated_data.get("email"),
                movie_id=validated_data.get("movie_id"),
            )
            for seat_id in validated_data.get("seat_ids")
        ]
        return BooekedTheaterSeat.objects.bulk_create(booked_seats)
