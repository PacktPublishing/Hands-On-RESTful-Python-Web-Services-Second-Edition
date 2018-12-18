import pytest
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from games import views
from games.models import EsrbRating
from games.models import Player


def create_esrb_rating(client, description):
    url = reverse(views.EsrbRatingList.name)
    esrb_rating_data = {'description': description}
    esrb_rating_response = client.post(url, esrb_rating_data, format='json')
    return esrb_rating_response


@pytest.mark.django_db
def test_create_and_retrieve_esrb_rating(client):
    """
    Ensure we can create a new EsrbRating and then retrieve it
    """
    new_esrb_rating_description = 'E (Everyone)'
    response = create_esrb_rating(client, new_esrb_rating_description)
    assert response.status_code == status.HTTP_201_CREATED
    assert EsrbRating.objects.count() == 1
    assert EsrbRating.objects.get().description == new_esrb_rating_description


@pytest.mark.django_db
def test_create_duplicated_esrb_rating(client):
    """
    Ensure we can create a new EsrbRating
    """
    url = reverse('esrbrating-list')
    new_esrb_rating_description = 'T (Teen)'
    post_response_1 = create_esrb_rating(client, new_esrb_rating_description)
    assert post_response_1.status_code == status.HTTP_201_CREATED
    post_response_2 = create_esrb_rating(client, new_esrb_rating_description)
    assert post_response_2.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_esrb_ratings_list(client):
    """
    Ensure we can retrieve an ESRB rating
    """
    new_esrb_rating_description = 'AO (Adults Only)'
    post_response = create_esrb_rating(client, new_esrb_rating_description)
    url = reverse('esrbrating-list')
    get_response = client.get(url, format='json')
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data['count'] == 1
    assert get_response.data['results'][0]['description'] == new_esrb_rating_description


@pytest.mark.django_db
def test_update_game_category(client):
    """
    Ensure we can update a single field for an ESRB rating
    """
    new_esrb_rating_description = 'M (Mature)'
    post_response = create_esrb_rating(client, new_esrb_rating_description)
    url = reverse('esrbrating-detail', None, {post_response.data['id']})
    updated_esrb_rating_description = 'M10 (Mature - 10)'
    data = {'description': updated_esrb_rating_description}
    patch_response = client.patch(url, 
        data, 
        content_type='application/json',
        format='json')
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_response.data['description'] == updated_esrb_rating_description


@pytest.mark.django_db
def test_filter_esrb_rating_by_description(client):
    """
    Ensure we can filter an ESRB rating by description
    """
    esrb_rating_description1 = 'T (Teen)'
    create_esrb_rating(client, esrb_rating_description1)
    esrb_rating_description2 = 'M (Mature)'
    create_esrb_rating(client, esrb_rating_description2)
    filter_by_description = { 'description' : esrb_rating_description1 }
    url = '{0}?{1}'.format(reverse('esrbrating-list'),
        urlencode(filter_by_description))
    get_response = client.get(url, format='json')
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data['count'] == 1
    assert get_response.data['results'][0]['description'] == esrb_rating_description1
