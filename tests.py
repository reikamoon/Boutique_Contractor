from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_product_id = ObjectId('5dedab57cc9f102278e83b40')
sample_product = {
    'name': 'Sample Gown',
    'price': '$25.99',
    'image_url': 'https://i.pinimg.com/originals/c3/32/bf/c332bfa1e0a53c882c8c352181aa7832.jpg'

}
sample_form_data = {
    'name': sample_product['name'],
    'price': sample_product['price'],
    'image_url': sample_product['image_url']
}

class ClothesTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Lolita', result.data)

    def test_new(self):
        """Test the new entry page."""
        result = self.client.get('/catalogue/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Add a Product', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_product(self, mock_find):
        """Test showing a single product."""
        mock_find.return_value = sample_product

        result = self.client.get(f'/catalogue/{sample_product_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Sample Gown', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_product(self, mock_find):
        """Test editing a single product."""
        mock_find.return_value = sample_product

        result = self.client.get(f'edit/{sample_product_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'$25.99', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_product(self, mock_insert):
        """Test submitting a new product."""
        result = self.client.post('/catalogue', data=sample_form_data)

        # After submitting, should redirect to that product's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_product)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_product(self, mock_update):
        result = self.client.post(f'/catalogue/{sample_product_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_product_id}, {'$set': sample_product})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_product(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/delete/{sample_product_id}', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_product_id})

if __name__ == '__main__':
    unittest_main()
